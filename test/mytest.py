'''
Author: zyq
Date: 2024-04-02 11:31:00
LastEditTime: 2024-04-07 16:42:25
FilePath: /LLMFastApiService/test/mytest.py
Description: for test

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import random
import string
import hashlib
from service.cogagent_service import load_model, do_infer
    
if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(os.path.dirname(os.path.dirname(__file__)))
    
    # cogagent test
    model_path = '/home/kemove/zyq/giit/LLMFastApiService/models/cogagent-chat-hf'
    tokenizer_path = '/home/kemove/zyq/giit/LLMFastApiService/models/tokenizer/vicuna-7b-v1.5'
    img_path = '/home/kemove/d0379008b7eda5f1d456f6e06c3a66bb.jpeg'
    query = 'describe the img'

    model, tokenizer = load_model(model_path, tokenizer_path)
    resp, history = do_infer(img_path, query, model, tokenizer)
    
    print(resp)
    print('-----')
    print(history)
    