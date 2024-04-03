# LLMFastApiService
## 简介
LLMFASTAPISERVICE是一个基于FastApi开发，用于托管模型并提供多轮对话的后台服务框架，目前主要封装的模型类型有:
* 视觉大模型
* 非fastchat服务所托管的模型。fastchat服务: https://github.com/lm-sys/FastChat
* 其他业务小模型

已集成模型列表:
* Qilin-Med-VL: https://github.com/williamliujl/Qilin-Med-VL

## 快速开始
### 安装依赖
* 创建conda环境: `conda create -n py39-fastapi python=3.9`
* 安装相关依赖: `pip install -r requirements.txt`

### 启动服务
两种拉起服务的方式:
* 终端拉起服务，服务日志输出到当前控制台上。执行命令: `python startup.py`
* 后台拉起服务，服务日志在~/LLMFastApiService/logs/目录的startup_log.txt。执行命令: `bash startup.sh`

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

shell脚本文件说明:
* startup.sh: 启动服务脚本, `bash startup.sh`
* kill.sh: 关闭指定端口的进程，`bash kill.sh`

## 视觉模型api调用流程
* 步骤:加载模型或上传目标图像(load_model or upload_image) ---> 多轮对话, 模型推理(infer) ---> 释放模型(release_model)
* 每个会话结束后需要释放模型，防止模型占用显卡资源过多
