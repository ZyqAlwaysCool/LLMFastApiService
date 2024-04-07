'''
Author: zyq
Date: 2024-04-02 15:23:29
LastEditTime: 2024-04-07 17:51:39
FilePath: /LLMFastApiService/app/cogagent_app.py
Description: fastapi app, for cogagent

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, HTTPException
from typing import Union
from pydantic import BaseModel, Field
import uvicorn
import torch

from utils.logs.logger import load_logger
from utils.utils import generate_unique_string
from service.cogagent_service import load_model, do_infer
from infra.model_define import BaseResponse, InferCogRequest

cog_logger = load_logger()

# app define
class CogVLMApp:
    def __init__(self, model_path: str, tokenizer_path: str):
        self.__is_loaded = False
        self.__model_path = model_path
        self.__tokenzier_path = tokenizer_path
        self.__model_dct = {}
        self.__history = []
    
    def __mount_app_route(self, app: FastAPI):
        @app.get("/chatCogVLM/loadModel", tags=['Chat'], summary='加载CogVLM模型')
        async def load_cog_vlm():
            if self.__is_loaded:
                cog_logger.info('cogVLM is already loaded. just return 0')
            else:
                model, tokenizer = load_model(self.__model_path, self.__tokenzier_path)
                self.__model_dct['tokenizer'] = tokenizer
                self.__model_dct['model'] = model
                self.__is_loaded = True
                cog_logger.info('cogVLM load succ.')
            return BaseResponse(msg='load cogVlm model succ')
        
        @app.post("/chatcogVLM/infer", tags=['Chat'], summary='推理cogVLM模型')
        async def infer(req: InferCogRequest):
            if not self.__is_loaded:
                cog_logger.error('cogVlM is not loaded. please load first.')
                return BaseResponse(code=1, msg="cogVLM is not loaded. please load first.")

            tokenizer = self.__model_dct['tokenizer']
            model = self.__model_dct['model']
            resp = do_infer(req.imgpath, req.query, self.__history, model, tokenizer)
            return BaseResponse(data={'answer': resp})
        
        @app.get("/chatCogVLM/clearHistory", tags=['Chat'], summary='清空对话历史记录')
        async def clear_chat_history():
            self.__history = []
            cog_logger.info('clear cogVLM chat record history')
            return BaseResponse(msg="clear cogVLM chat record history, you can chat with other img.")
        
        @app.post("/chatCogVLM/uploadImg", tags=['Tool'], summary='上传图片')
        async def upload_img(img: UploadFile):
            # 验证文件类型, 仅支持jpeg, jpg, png
            allowed_content_types = ["image/jpeg", "image/jpg", "image/png"]
            if img.content_type not in allowed_content_types:
                raise HTTPException(status_code=415, detail=f"Unsupported media type. Expected one of {allowed_content_types}, received {img.content_type}.")
            
            # 获取文件内容
            contents = await img.read()
            origin_filename = img.filename
            _, file_ext = os.path.splitext(origin_filename)
            new_filename = generate_unique_string('cogVLM_') + file_ext
            save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/resources', new_filename)
            with open(save_path, 'wb') as f:
                f.write(contents)

            self.__is_first_chat = True
            file_info = {"filename": new_filename, "content_type": img.content_type, "saved_path": save_path}
            return BaseResponse(code=0, msg="success", data=file_info)
                        
    def create_cogvlm_app(self):
        cog_logger.info('start cogVLM app')
        app = FastAPI(title='CogVLM API Server')
        self.__mount_app_route(app)
        return app
