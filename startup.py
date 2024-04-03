'''
Author: zyq
Date: 2024-04-02 10:32:49
LastEditTime: 2024-04-03 11:46:44
FilePath: /LLMFastApiService/startup.py
Description: 后台入口

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import uvicorn

from app.qilin_app import MedVlmApp
from configs.server_config import get_server_config

def create_med_app(model_name: str = 'qilin_med_vlm'):
    model_path = '/home/kemove/zyq/giit/LLMFastApiService/models/Qilin-Med-VL-Chat'
    my_app = MedVlmApp(model_path).create_medvlm_app()
    model_server_config = get_server_config(model_name)
    uvicorn.run(my_app, host=model_server_config['host'], port=model_server_config['port'])

if __name__ == '__main__':
    create_med_app()