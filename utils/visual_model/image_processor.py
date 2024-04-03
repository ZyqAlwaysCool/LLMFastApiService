'''
Author: zyq
Date: 2024-04-02 14:53:56
LastEditTime: 2024-04-02 14:56:14
FilePath: /LLMFastApiService/utils/visual_model/image_processor.py
Description: image processor

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''


from PIL import Image
from io import BytesIO
from utils.logs.logger import load_logger

image_logger = load_logger()

def load_image(image_file):
    image_logger.info("start load image. file path=({})".format(image_file))
    return Image.open(image_file).convert('RGB')