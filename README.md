# Medical Dataset Copilot

✨ **大语言模型(LLM)数据分析智能体**
支持任意数据集和描述文档一键智能导入与智能图表绘制，通过多智能体协作和上下文长数据记忆，实现精准的自然语言查询与可视化分析。
基于医学影像数据集的行业应用，支持从行业数据网站智能爬取专业知识信息，导出专业数据分析报告。

🚩[English Readme](./README.en.md)

[个人网站：www.bytesc.top](http://www.bytesc.top)



## 功能简介

- 1, 基于代码生成的大语言模型智能体(AI Agent)，实现数据查询智能绘制多种统计图表
- 2, 实现智能体对用户的反问，解决用户提问模糊、不完整的情况
- 3, 智能体支持灵活的自定义函数调用(function call)和思维链(COT)
- 4, 实现多智能体的合作调用，能够处理大语言模型表现不稳定等异常情况
- 5, 上下文支持非文本长数据记忆，在多轮对话当中实现数据的存取
- 6, 支持用户私有数据表格一键导入数据库，支持上传文档生成数据注释标注
- 7, 根据用户提供的网页链接，智能爬取动态网页内容，自动提取结构化知识，用于数据标注、背景补充和领域知识增强 

## 技术架构

### 核心组件与技术架构

#### **1. 动态工具调用的函数图谱（Function Graph）**  
- 智能选择最佳工具链，根据任务类型动态组合数据查询、分析与可视化功能。  

#### **2. 意图讨论和问题拆解** 
- 将复杂问题拆解为子任务列表(To-do List)，智能体逐个解决
- 支持反问用户澄清模糊或不完整的需求

#### **3. 成功历史蒸馏** 
- 基于历史成功对话蒸馏知识库，新提问时检索相似案例
- 将成功经验作为示例注入当前对话，借鉴以往解决思路

#### **4. 多智能体协作层**  
- 通过角色化Agent分工（如数据查询Agent、校验Agent、报告生成Agent）实现复杂任务流水线处理。  
 
#### **5. 用户私有数据导入与专业知识爬取**  
- 用户私有数据导入：支持任意CSV文件一键导入数据库，配合数据描述文档，通过数据标注Agent自动生成字段注释，实现无结构化数据的快速解析与查询。
- 专业知识爬取：根据用户提供的网页链接，智能爬取动态网页内容，自动提取结构化知识，用于数据标注、背景补充和领域知识增强。 


### 工作流程

![](./readme_img/flow2.png)

基本流程：
User query → History Search → Solution breakdown → Function selection → Code generation → Execution → Validation
1. **Question**: 用户自然语言问题提问
2. **History Search**: 根据历史成功对话蒸馏知识库，在提问时搜索知识库，借鉴以往成功思路
3. **Solution breakdown**: 和用户讨论意图，制定解决方案，把复杂问题拆解为子任务列表(To-do List)，智能体逐个解决小问题，最终实现复杂任务的解决。
4. **Function Selection**: LLM 根据函数基本信息选择多个函数，通过函数依赖图(Function Graph)获得可用函数列表和详细注释（函数包括非智能体函数(Custum Function)和调用其它智能体的函数(Agent as Function)，实现多智能体协同）
5. **Function Skill**: 根据 function 的选择动态提供不同的 prompt 信息(借鉴 skill 的概念)
6. **Function Calls Chain**: LLM 根据函数列表和详细注释，生成调用多个函数的 python 代码并执行
7. **Result Review**: LLM 回顾总结整个流程，评估问题是否解决，更新任务列表，没有解决则反问用户，使其澄清问题或者提供更多信息


### 用户私有数据导入

任意 csv 文件，加上描述数据的文档即可被解析查询

![](./readme_img/flow4.png)

1. 上传 csv 文件自动导入数据库
2. 上传数据描述文档调用数据标注 Agent 生成数据注释

### 专业知识爬取

![](./readme_img/fetch_url.png)

根据用户提供的网页链接，智能爬取动态网页，实现知识获取和数据标注。

### 上下文数据传递

数据的上下文传递和中期记忆

![](./readme_img/flow3.png)

1. Agent 生成代码调用 sql agent 查询数据，查询结果自动保存为 csv 文件，文件链接存入上下文
2. 下一轮对话中 Agent 从上下文中获取 csv 数据文件链接，生成代码可以通过链接重新读取数据


### 演示

支持 api 接口调用和图形界面

![](./readme_img/demo.png)

用户私有数据导入与专业知识爬取

📹 [演示视频](./readme_img/demo_video01.mp4)

<video src="./readme_img/demo_video01.mp4" controls width="100%">
  您的浏览器不支持视频播放
</video>

智能数据分析问答和分析报告生成

![](./readme_img/demo2.1.png)

![](./readme_img/demo2.2.png)

![](./readme_img/demo3.1.png)

![](./readme_img/demo3.2.png)

数据分析智能问答

📹 [演示视频](./readme_img/demo_2-1.mp4)

<video src="./readme_img/demo_2-1.mp4" controls width="100%">
  您的浏览器不支持视频播放
</video>

连续对话和用户需求修正

📹 [演示视频](./readme_img/demo_2-2.mp4)

<video src="./readme_img/demo_2-2.mp4" controls width="100%">
  您的浏览器不支持视频播放
</video>

数据分析报告文件导出

📹 [演示视频](./readme_img/demo_2-3.mp4)

<video src="./readme_img/demo_2-3.mp4" controls width="100%">
  您的浏览器不支持视频播放
</video>

## 如何使用

### 安装依赖

python 版本 3.10

```bash
pip install -r requirement.txt
```

### 配置文件

`./config/config.yaml`
```yml
# config
server_port: 8009 # 部署端口
server_host: "0.0.0.0"  # allow host
# 数据库
mysql: "mysql+pymysql://root:123456@localhost:3306/singapore_land"

# 静态文件服务地址，本机域名/ip:端口
static_path: "http://127.0.0.1:8009/"

model_name: "qwen-max"
# glm-4
# deepseek-chat
# qwen-max
# gpt-4o-mini

model_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
# https://open.bigmodel.cn/api/paas/v4/
# https://api.deepseek.com/v1/
# https://dashscope.aliyuncs.com/compatible-mode/v1
# https://api.openai.com/v1

```

### 大语言模型配置

新建文件：`agent\utils\llm_access\api_key_openai.txt` 在其中填写`api-key`

`api-key`获取链接：
- 阿里云:[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)
- deepseek:[https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)
- glm:[https://open.bigmodel.cn/](https://open.bigmodel.cn/)

### 运行

#### 服务端

```bash
# 服务端
python ./main.py
```

启动后可以通过api访问服务

#### 前端

项目自带一个简单的pywebio图形界面

```bash
# 启动前端服务
python ./front.py
```

# 开源许可证

此翻译版本仅供参考，以 LICENSE 文件中的英文版本为准

MIT 开源许可证：

版权所有 (c) 2025 bytesc

特此授权，免费向任何获得本软件及相关文档文件（以下简称“软件”）副本的人提供使用、复制、修改、合并、出版、发行、再许可和/或销售软件的权利，但须遵守以下条件：

上述版权声明和本许可声明应包含在所有副本或实质性部分中。

本软件按“原样”提供，不作任何明示或暗示的保证，包括但不限于适销性、特定用途适用性和非侵权性。在任何情况下，作者或版权持有人均不对因使用本软件而产生的任何索赔、损害或其他责任负责，无论是在合同、侵权或其他方面。
