<!--
 * @Author: zyq
 * @Date: 2024-04-02 10:32:16
 * @LastEditTime: 2024-06-17 15:15:17
 * @FilePath: /LLMFastApiService/README.md
 * @Description: describe file
 * 
 * Copyright (c) 2024 by zyq, All Rights Reserved. 
-->
# LLMFastApiService
## 简介
LLMFASTAPISERVICE是一个基于FastApi开发，用于托管模型并提供多轮对话的后台服务框架，目前主要封装的模型类型有:
* 视觉大模型
* 非[fastchat](https://github.com/lm-sys/FastChat)服务所托管的模型。
* 其他业务小模型

已集成模型列表:
* Qilin-Med-VL: https://github.com/williamliujl/Qilin-Med-VL
* cogagent-chat-hf: https://huggingface.co/THUDM/cogagent-chat-hf

## 快速开始
### 安装依赖
* 创建conda环境: `conda create -n py39-fastapi python=3.9`
* 安装相关依赖: `pip install -r requirements.txt`
* 模型文件需自行下载，存放在models目录下

### 启动服务
* 下载模型文件， 存放在models目录下
* 修改server_config.py中的配置信息，配置模型本地路径、端口等信息
* 拉起服务
  * 终端拉起服务，服务日志输出到当前控制台上。执行命令: `python startup.py`
  * 后台拉起服务，服务日志在~/LLMFastApiService/logs/目录的startup_log_xxx_app.txt。在startup文件夹里针对不同模型拉起对相应app，命令: `bash startup_xxx_app.sh`

服务拉起后, 可以通过浏览器访问: http://{your_host}:{your_port}/docs 查看api接口说明

## 项目结构
LLMFastApiService的项目结构如下:
* app: 每个模型包含一个app.py文件，该文件定义了模型相关的fastapi接口。新增模型需要相应增加一个xxx_app.py
* configs: 统一管理模型配置，包含模型文件路径、模型服务挂载端口、挂载cuda卡等配置信息
* infra: 定义请求响应与回包的数据结构(基于Pydantic)、数据库等基础设施配置
* logs: 服务日志，包含启动日志、请求响应日志
* models: 存储本地模型数据文件
* resources: 存储模型服务推理时候的资源文件，如视觉模型对话的具体图片信息
* service: 定义模型的推理服务，一般包括模型加载、模型推理等操作逻辑
* test: 服务测试
* utils: 定义工具函数，包括: 视觉模型工具函数、语言模型工具函数、通用工具函数以及模型依赖的第三方库
* startup: 存放各模型的服务启动入口，由于各模型对于torch、transformers等库的依赖版本不同，因此针对不同的模型需要创建不同的启动脚本startup.py，命名方式: `startup_{model_name}.py`

shell脚本文件说明:
* startup.sh: 启动服务脚本, `bash startup.sh`
* kill.sh: 关闭指定端口的进程，`bash kill.sh`

## 视觉模型api调用流程
* 步骤:加载模型或上传目标图像(load_model or upload_image) ---> 多轮对话, 模型推理(infer) ---> 释放模型(release_model)
* 每个会话结束后需要释放模型，防止模型占用显卡资源过多
