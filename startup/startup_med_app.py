'''
Author: zyq
Date: 2024-04-02 10:32:49
LastEditTime: 2024-04-07 18:02:20
FilePath: /LLMFastApiService/startup_med_app.py
Description: med-vlm后台入口, 需要切py39-fastapi, transformers版本为4.28.1

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import uvicorn

from app.qilin_app import MedVLMApp
from configs.server_config import get_server_config

def create_med_app(model_name: str = 'qilin_med_vlm'):
    model_server_config = get_server_config(model_name)
    model_path = model_server_config['model_path']
    my_app = MedVLMApp(model_path).create_medvlm_app()
    uvicorn.run(my_app, host=model_server_config['host'], port=model_server_config['port'])

if __name__ == '__main__':
    create_med_app()