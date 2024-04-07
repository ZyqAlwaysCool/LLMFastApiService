'''
Author: zyq
Date: 2024-04-02 15:12:10
LastEditTime: 2024-04-07 17:07:52
FilePath: /LLMFastApiService/app/qilin_app.py
Description: fastapi app, for qilin-med-vl

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
from service.qilin_med_service import load_model, do_infer, load_image, process_images
from infra.model_define import BaseResponse, InferVLMRequest

med_logger = load_logger()

# app define
class MedVLMApp:
    def __init__(self, model_path: str):
        self.__is_loaded = False
        self.__model_path = model_path
        self.__model_dct = {}
        self.__is_first_chat = True
    
    def __mount_app_route(self, app: FastAPI):
        @app.get("/chatMedVLM/loadModel", tags=['Chat'], summary='加载MedVLM模型')
        async def load_med_vlm():
            if self.__is_loaded:
                med_logger.info('medVlm is already loaded. just return 0')
            else:
                tokenizer, model, image_processor, conv = load_model(self.__model_path)
                self.__model_dct['tokenizer'] = tokenizer
                self.__model_dct['model'] = model
                self.__model_dct['image_processor'] = image_processor
                self.__model_dct['conv'] = conv
                self.__is_loaded = True
                self.__is_first_chat = True
                med_logger.info('medVlm load succ.')
            return BaseResponse(msg='load medVlm model succ')
        
        @app.post("/chatMedVLM/infer", tags=['Chat'], summary='推理MedVLM模型')
        async def infer(req: InferVLMRequest):
            if not self.__is_loaded:
                med_logger.error('medVLM is not loaded. please load first.')
                return BaseResponse(code=1, msg="medVlm is not loaded. please load first.")

            tokenizer = self.__model_dct['tokenizer']
            model = self.__model_dct['model']
            image_processor = self.__model_dct['image_processor']
            conv = self.__model_dct['conv']
            
            image = load_image(req.imgpath)
            if image is None:
                med_logger.error('load image failed.')
                return BaseResponse(code=1, msg="load image failed.")
            image_tensor = process_images([image], image_processor, None)
            if type(image_tensor) is list:
                image_tensor = [image.to(model.device, dtype=torch.float16) for image in image_tensor]
            else:
                image_tensor = image_tensor.to(model.device, dtype=torch.float16)
            
            real_img = None
            if self.__is_first_chat:
                real_img = image
            
            ans = do_infer(tokenizer, model, image_processor, conv, image_tensor, real_img, req.query)
            self.__is_first_chat = False
            
            return BaseResponse(data={'answer': ans})
        
        @app.get("/chatMedVLM/releaseModel", tags=['Chat'], summary='卸载模型')
        async def release_model():
            self.__model_dct.clear()
            torch.cuda.empty_cache()
            self.__is_loaded = False
            med_logger.info('medVlm is release. if want infer, should reload.')
            return BaseResponse(msg="release medVLM succ.")
        
        @app.post("/chatMedVLM/uploadImg", tags=['Tool'], summary='上传图片')
        async def upload_img(img: UploadFile):
            # 验证文件类型, 仅支持jpeg, jpg, png
            allowed_content_types = ["image/jpeg", "image/jpg", "image/png"]
            if img.content_type not in allowed_content_types:
                raise HTTPException(status_code=415, detail=f"Unsupported media type. Expected one of {allowed_content_types}, received {img.content_type}.")
            
            # 获取文件内容
            contents = await img.read()
            origin_filename = img.filename
            _, file_ext = os.path.splitext(origin_filename)
            new_filename = generate_unique_string() + file_ext
            save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/resources', new_filename)
            with open(save_path, 'wb') as f:
                f.write(contents)

            self.__is_first_chat = True
            file_info = {"filename": new_filename, "content_type": img.content_type, "saved_path": save_path}
            return BaseResponse(code=0, msg="success", data=file_info)
                        
    def create_medvlm_app(self):
        med_logger.info('start medVLM app')
        app = FastAPI(title='MedVlm API Server')
        self.__mount_app_route(app)
        return app
