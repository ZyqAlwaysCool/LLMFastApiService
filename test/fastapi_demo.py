'''
Author: zyq
Date: 2024-03-25 10:27:11
LastEditTime: 2024-04-02 10:33:12
FilePath: /LLMFastApiService/fastapi_demo.py
Description: describe file

Copyright (c) 2024 by zyq, All Rights Reserved. 
'''
from typing import Optional
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field
import logging
import uvicorn

#日志库设置
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler() #输入屏幕
fh = logging.FileHandler(filename='./server.log') #输入到日志里
formatter = logging.Formatter("%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

def cal(test_lst: list):
    return sum(test_lst)

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(title="this is a path params: item", ge=10),
              q: str = Query(default="this is a default q", max_length=10, min_length=3, alias="items-query-params")):
    test_list = [i for i in range(1000000)]
    rest = cal(test_list)
    return {"item_id": item_id, "q": q, "rest": rest}

@app.get("/file/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/queryparams/")
def query_params(query: int, params: str, skip: int = 0, limit: Optional[str] = None):
    return {"query": query, "params": params, "skip": skip, "limit": limit}


# post
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(ge=10, title="price should greater than 10")
    tax: Optional[str] = None
    
class LLMModel(BaseModel):
    name: str
    img: str
    
@app.post("/items/")
def create_items(item: Item, llm_model: LLMModel):
    logger.info("item.name=({})".format(item.name))
    return item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=22000)