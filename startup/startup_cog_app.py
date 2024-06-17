'''
Author: zyq
Date: 2024-04-02 10:32:49
LastEditTime: 2024-04-08 11:48:28
FilePath: /LLMFastApiService/startup/startup_cog_app.py
Description: 后台入口, py311-dev

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.cogagent_app import CogVLMApp
from configs.server_config import get_server_config

def create_cog_app(model_name: str = 'cog_vlm'):
    model_server_config = get_server_config(model_name)
    model_path = model_server_config['model_path']
    tokenizer_path = model_server_config['tokenizer_path']
    my_app = CogVLMApp(model_path, tokenizer_path).create_cogvlm_app()
    uvicorn.run(my_app, host=model_server_config['host'], port=model_server_config['port'])

if __name__ == '__main__':
    create_cog_app()