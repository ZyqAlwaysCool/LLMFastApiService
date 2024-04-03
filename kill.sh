#!/bin/bash
###
 # @Author: zyq
 # @Date: 2024-04-01 14:59:21
 # @LastEditTime: 2024-04-03 11:52:47
 # @FilePath: /LLMFastApiService/kill.sh
 # @Description: 该脚本用于检查指定端口号是否有进程在使用,如果有则kill掉. 运行: bash kill.sh
 # 
 # Copyright (c) 2024 by zyq, All Rights Reserved. 
### 


# 读取用户输入的端口号
read -p "Enter the port number: " port_number

# 检查指定端口是否有进程在使用
check_process() {
    local port=$1
    # 使用 lsof 命令查找指定端口的进程，并获取进程ID
    local pid=$(lsof -ti :$port)
    if [ -n "$pid" ]; then
        # 如果找到对应的进程，则输出提示信息并杀死进程
        echo "Process found on port $port with PID: $pid"
        echo "Killing process..."
        kill $pid
        echo "Process killed."
    else
        # 如果没有找到对应的进程，则输出提示信息
        echo "No process found on port $port."
    fi
}

# 调用函数检查指定端口是否有进程在使用
check_process $port_number
