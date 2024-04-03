'''
Author: zyq
Date: 2024-04-02 11:31:00
LastEditTime: 2024-04-03 15:12:24
FilePath: /LLMFastApiService/test/mytest.py
Description: for test

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import time
import os
import sys
import random
import string
import hashlib
sys.path.append('..')
    
if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(os.path.dirname(os.path.dirname(__file__)))
    _, file_ext = os.path.splitext('hello.txt')