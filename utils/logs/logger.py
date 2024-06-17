'''
Author: zyq
Date: 2024-04-02 11:28:37
LastEditTime: 2024-04-08 11:46:43
FilePath: /LLMFastApiService/utils/logs/logger.py
Description: logger loader

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import os
import logging
from datetime import datetime

def load_logger():
    # 设置日志输出路径为'~/LLMFastApiService/logs'
    #current_dir = os.getcwd()
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if not current_dir.endswith('LLMFastApiService'):
        raise ValueError('Current working directory does not end with "LLMFastApiService"')
        
    
    # 获取当前日期
    current_date = datetime.now().date()
    
    log_filename = current_dir + '/logs/' + str(current_date) + '-server.log' #日志以天为单位缓存
    
    #日志库设置
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_filename) #输入到日志里
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger
