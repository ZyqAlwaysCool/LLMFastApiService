'''
Author: zyq
Date: 2024-04-03 10:55:22
LastEditTime: 2024-04-03 10:58:53
FilePath: /LLMFastApiService/infra/model_define.py
Description: 定义请求的输入输出模型

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    """
    基础响应模型定义
    """
    code: int = Field(0, description="响应状态码")
    msg: str = Field("success", description="响应消息")
    data: dict = Field({}, description="响应数据")

class InferVLMRequest(BaseModel):
    '''
    视觉模型推理请求定义
    '''
    query: str = Field(min_length=1, max_length=1024)
    imgpath: str

class InferCogRequest(BaseModel):
    '''
    cogagent模型推理请求定义
    '''
    query: str = Field(min_length=1, max_length=1024)
    imgpath: str