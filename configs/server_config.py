'''
Author: zyq
Date: 2024-04-03 11:34:21
LastEditTime: 2024-04-07 17:55:44
FilePath: /LLMFastApiService/configs/server_config.py
Description: 服务端配置, 模型路径需改为本地路径

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''


LLM_SERVER_CONFIG = {
    'qilin_med_vlm' : {'model_path': '/home/kemove/zyq/giit/LLMFastApiService/models/Qilin-Med-VL-Chat',
                       'cuda': '3',
                       'port': 22002,
                       'host': '0.0.0.0',
                       },
    'cog_vlm' : {'model_path': '/home/kemove/zyq/giit/LLMFastApiService/models/cogagent-chat-hf',
                 'cuda': '4',
                 'port': 22001,
                 'host': '0.0.0.0',
                 'tokenizer_path': '/home/kemove/zyq/giit/LLMFastApiService/models/tokenizer/vicuna-7b-v1.5',
                  },
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
