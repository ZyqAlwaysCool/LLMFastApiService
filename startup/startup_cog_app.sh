###
 # @Author: zyq
 # @Date: 2024-04-03 11:51:18
 # @LastEditTime: 2024-04-08 11:41:43
 # @FilePath: /LLMFastApiService/startup/startup_cog_app.sh
 # @Description: describe file
 # 
 # Copyright (c) 2024 by zyq, All Rights Reserved. 
### 

python startup_cog_app.py > ../logs/startup_log_cog_app.txt 2>&1 &
echo 'llm service cogVLM started.'
