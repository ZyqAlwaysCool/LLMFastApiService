'''
Author: zyq
Date: 2024-04-07 16:10:04
LastEditTime: 2024-04-07 17:41:36
FilePath: /LLMFastApiService/service/cogagent_service.py
Description: cogagent视觉模型服务, 使用4bit量化加载, fp16精度

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

from configs.server_config import get_server_config

import os
os.environ['CUDA_VISIBLE_DEVICES'] = get_server_config('cog_vlm')['cuda']

import torch
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PIL import Image
from transformers import AutoModelForCausalLM, LlamaTokenizer
import argparse
from accelerate import init_empty_weights, infer_auto_device_map, load_checkpoint_and_dispatch
from utils.logs.logger import load_logger

cog_logger = load_logger()

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
torch_type = torch.float16

def load_model(model_path: str, tokenizer_path: str):
    if DEVICE == 'cpu':
        cog_logger.error('No GPU available, please check.')
        return -1
    
    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch_type,
        low_cpu_mem_usage=True,
        load_in_4bit=True,
        trust_remote_code=True
    ).eval()
    
    return model, tokenizer

def do_infer(image_path: str, query: str, history: list, model, tokenizer):
    if DEVICE == 'cpu':
        cog_logger.error('No GPU available, please check.')
        return -1

    if query == 'endInfer':
        del model
        torch.cuda.empty_cache()
        return 'endInfer'

    chat_image = Image.open(image_path).convert('RGB')
    input_by_model = model.build_conversation_input_ids(tokenizer, query=query, history=history, images=[chat_image])
    inputs = {
        'input_ids': input_by_model['input_ids'].unsqueeze(0).to(DEVICE),
        'token_type_ids': input_by_model['token_type_ids'].unsqueeze(0).to(DEVICE),
        'attention_mask': input_by_model['attention_mask'].unsqueeze(0).to(),
        'images': [[input_by_model['images'][0].to(DEVICE).to(torch_type)]],
    }
    if 'cross_images' in input_by_model and input_by_model['cross_images']:
        inputs['cross_images'] = [[input_by_model['cross_images'][0].to(DEVICE).to(torch_type)]]
    
    gen_kwargs = {"max_length": 2048,
                    "temperature": 0.9,
                    "do_sample": False}
    
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        response = tokenizer.decode(outputs[0])
        response = response.split("</s>")[0]
        history.append((query, response))

    cog_logger.info('history=({})'.format(history))
    return response
    