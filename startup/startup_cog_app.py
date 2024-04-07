'''
Author: zyq
Date: 2024-04-02 10:32:49
LastEditTime: 2024-04-07 17:22:44
FilePath: /LLMFastApiService/startup.py
Description: 后台入口

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import uvicorn

# from app.qilin_app import MedVlmApp
from app.cogagent_app import CogVLMApp
from configs.server_config import get_server_config

# def create_med_app(model_name: str = 'qilin_med_vlm'):
#     model_server_config = get_server_config(model_name)
#     model_path = model_server_config['model_path']
#     my_app = MedVlmApp(model_path).create_medvlm_app()
#     uvicorn.run(my_app, host=model_server_config['host'], port=model_server_config['port'])

def create_cog_app(model_name: str = 'cog_vlm'):
    model_server_config = get_server_config(model_name)
    model_path = model_server_config['model_path']
    tokenizer_path = model_server_config['tokenizer_path']
    my_app = CogVLMApp(model_path, tokenizer_path).create_cogvlm_app()
    uvicorn.run(my_app, host=model_server_config['host'], port=model_server_config['port'])

if __name__ == '__main__':
    #create_med_app()
    create_cog_app()