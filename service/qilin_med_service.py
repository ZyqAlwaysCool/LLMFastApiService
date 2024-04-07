'''
Author: zyq
Date: 2024-04-02 11:13:49
LastEditTime: 2024-04-07 17:55:33
FilePath: /LLMFastApiService/service/qilin_med_service.py
Description: qilin_med_vlm服务

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

from configs.server_config import get_server_config

import os
os.environ['CUDA_VISIBLE_DEVICES'] = get_server_config('qilin_med_vlm')['cuda']

# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '5'

import torch
import sys
sys.path.append('..')

from utils.llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from utils.llava.conversation import conv_templates, SeparatorStyle
from utils.llava.model.builder import load_pretrained_model
from utils.llava.utils import disable_torch_init
from utils.llava.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria
from utils.logs.logger import load_logger
from utils.visual_model.image_processor import load_image
from transformers import TextStreamer

mylogger = load_logger()

def load_model(model_path: str):
    disable_torch_init()
    model_name = 'llava-Qilin-Chat'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, None, model_name, False, False, device=device)

    conv_mode = 'llava_v1'
    conv = conv_templates[conv_mode].copy()
    roles = conv.roles
    
    return tokenizer, model, image_processor, conv

def do_infer(tokenizer, model, image_processor, conv, image_tensor, image, query):
    mylogger.info('do infer image=({})'.format(image))
    mylogger.info('do infer query=({})'.format(query))
   
    inp = query

    if image is not None:
        # first message
        if model.config.mm_use_im_start_end:
            inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + inp
        else:
            inp = DEFAULT_IMAGE_TOKEN + '\n' + inp
        conv.append_message(conv.roles[0], inp)
        image = None
    else:
        # later messages
        conv.append_message(conv.roles[0], inp)
    

    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()

    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
    stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
    keywords = [stop_str]
    stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            do_sample=True,
            temperature=0.4,
            max_new_tokens=512,
            streamer=streamer,
            use_cache=True,
            stopping_criteria=[stopping_criteria])

    outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()
    conv.messages[-1][-1] = outputs
    
    anwser = outputs.split('</s>')[0]
    return anwser
    
    