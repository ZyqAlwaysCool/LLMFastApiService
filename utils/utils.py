'''
Author: zyq
Date: 2024-04-03 09:10:17
LastEditTime: 2024-04-03 09:33:51
FilePath: /LLMFastApiService/utils/util.py
Description: 提供一系列工具函数

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import random
import string
import hashlib
import time

from utils.logs.logger import load_logger

util_logger = load_logger()

def generate_unique_string(prefix: str = 'uniquestr_'):
    # 获取当前时间戳（精确到秒）
    timestamp = int(time.time())
    # 生成随机字符串
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    # 将时间戳和随机字符串拼接起来
    unique_str = prefix + str(timestamp) + random_str
    md5_str = hashlib.md5(unique_str.encode()).hexdigest()[:16]
    util_logger.info('gen unique string=({})'.format(md5_str))
    return md5_str