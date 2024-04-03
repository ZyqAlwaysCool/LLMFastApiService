'''
Author: zyq
Date: 2024-04-03 11:34:21
LastEditTime: 2024-04-03 11:47:43
FilePath: /LLMFastApiService/configs/server_config.py
Description: 服务端配置

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''


LLM_SERVER_CONFIG = {
    'qilin_med_vlm' : {'model_path': '/home/kemove/zyq/giit/LLMFastApiService/models/Qilin-Med-VL-Chat',
                       'cuda': '1',
                       'port': 22000,
                       'host': '0.0.0.0'},
    'default' : {'model_path': '',
                 'cuda': '0',
                 'port': 8888,
                 'host': '0.0.0.0'}
}


def get_server_config(model_name: str):
    if model_name in LLM_SERVER_CONFIG.keys():
        return LLM_SERVER_CONFIG[model_name]
    else:
        return LLM_SERVER_CONFIG['default']
