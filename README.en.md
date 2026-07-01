# Medical Dataset Copilot

✨ **Medical Dataset Copilot - LLM Data Analysis Agent**  
Supports one-click intelligent import of arbitrary datasets and description documents, along with intelligent chart generation. Through multi-agent collaboration and long-context data memory, it enables precise natural language querying and visual analysis.  
Based on industry applications of medical imaging datasets, it supports intelligent crawling of professional knowledge from industry data websites and exports professional data analysis reports.

🚩[Personal Website: www.bytesc.top](http://www.bytesc.top)

## Features

- 1. Code-generation-based LLM AI Agent for data querying and intelligent plotting of various statistical charts
- 2. Agent-to-user clarification questioning to handle ambiguous or incomplete user queries
- 3. Flexible custom function calls and Chain of Thought (COT) support
- 4. Multi-agent collaborative invocation to handle instability and other anomalies in LLM outputs
- 5. Long-context support for non-text data memory, enabling data storage and retrieval across multi-turn dialogues
- 6. One-click import of user's private data tables into the database, with support for uploading documents to generate data annotation labels
- 7. Intelligent crawling of dynamic web content based on user-provided URLs, automatically extracting structured knowledge for data annotation, background supplementation, and domain knowledge enhancement

## Technical Architecture

### Core Components & Technical Architecture

#### **1. Dynamic Function Graph for Tool Invocation**  
- Intelligently selects the optimal tool chain, dynamically combining data query, analysis, and visualization functions based on task type.

#### **2. Intent Discussion & Problem Decomposition**  
- Breaks down complex problems into a to-do list of sub-tasks, which the agent solves one by one.
- Supports asking clarifying questions to users when requirements are vague or incomplete.

#### **3. Successful History Distillation**  
- Distills a knowledge base from historically successful dialogues; retrieves similar cases when new queries are raised.
- Injects successful experiences as examples into the current conversation to leverage prior solutions.

#### **4. Multi-Agent Collaboration Layer**  
- Uses role-based agents (e.g., Data Query Agent, Validation Agent, Report Generation Agent) to handle complex tasks in a pipeline.

#### **5. User Private Data Import & Professional Knowledge Crawling**  
- **User Private Data Import**: Supports one-click import of any CSV file into the database. With a data description document, a Data Annotation Agent automatically generates field comments, enabling rapid parsing and querying of unstructured data.  
- **Professional Knowledge Crawling**: Based on user-provided URLs, intelligently crawls dynamic web content and automatically extracts structured knowledge for data annotation, background supplementation, and domain knowledge enhancement.

### Workflow

![](./readme_img/flow2.png)

Basic Flow:
`User query → History Search → Solution breakdown → Function selection → Code generation → Execution → Validation`

1. **Question**: User asks a question in natural language.
2. **History Search**: Searches the distilled knowledge base from successful dialogues for relevant previous approaches.
3. **Solution breakdown**: Discusses intent with the user, formulates a solution plan, and breaks it down into a sub-task list (To-do List). The agent solves each sub-task one by one to achieve the overall complex objective.
4. **Function Selection**: The LLM selects multiple functions based on basic function information. The Function Graph provides a list of available functions with detailed comments (including both custom functions and Agent-as-Function invocations for multi-agent collaboration).
5. **Function Skill**: Dynamically provides different prompts based on the selected functions (drawing on the concept of "skills").
6. **Function Calls Chain**: The LLM generates and executes Python code that calls multiple functions based on the list and detailed descriptions.
7. **Result Review**: The LLM reviews and summarizes the entire process, assesses whether the problem is resolved, updates the task list, and asks clarifying questions if the problem remains unsolved.

### User Private Data Import

Any CSV file, along with a data description document, can be parsed and queried.

![](./readme_img/flow4.png)

1. Upload a CSV file for automatic database import.
2. Upload a data description document to invoke the Data Annotation Agent to generate data comments.

### Professional Knowledge Crawling

![](./readme_img/fetch_url.png)

Based on user-provided URLs, intelligently crawls dynamic web pages to acquire knowledge and support data annotation.

### Contextual Data Transfer

Contextual transfer and mid-term memory of data.

![](./readme_img/flow3.png)

1. The Agent generates code to invoke the SQL Agent for data queries. Query results are automatically saved as CSV files, and file links are stored in the context.
2. In subsequent dialogue turns, the Agent retrieves the CSV file link from the context and can read the data again via code.

### Demo

Supports both API calls and GUI.

![](./readme_img/demo.png)

User Private Data Import & Professional Knowledge Crawling

📹 [Demo Video](./readme_img/demo_video01.mp4)

<video src="./readme_img/demo_video01.mp4" controls width="100%">
  Your browser does not support the video tag.
</video>

Intelligent Data Q&A and Analysis Report Generation

![](./readme_img/demo2.1.png)

![](./readme_img/demo2.2.png)

![](./readme_img/demo3.1.png)

![](./readme_img/demo3.2.png)

Intelligent Data Q&A

📹 [Demo Video](./readme_img/demo_2-1.mp4)

<video src="./readme_img/demo_2-1.mp4" controls width="100%">
  Your browser does not support the video tag.
</video>

Multi-turn Dialogue and User Requirement Refinement

📹 [Demo Video](./readme_img/demo_2-2.mp4)

<video src="./readme_img/demo_2-2.mp4" controls width="100%">
  Your browser does not support the video tag.
</video>

Data Analysis Report Export

📹 [Demo Video](./readme_img/demo_2-3.mp4)

<video src="./readme_img/demo_2-3.mp4" controls width="100%">
  Your browser does not support the video tag.
</video>

## How to Use

### Install Dependencies

Python version 3.10

```bash
pip install -r requirement.txt
```

### Configuration File

`./config/config.yaml`
```yml
# config
server_port: 8009 # deployment port
server_host: "0.0.0.0"  # allow host
# database
mysql: "mysql+pymysql://root:123456@localhost:3306/singapore_land"

# static file service address, local machine domain/ip:port
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

### LLM Configuration

Create a file: `agent\utils\llm_access\api_key_openai.txt` and place your API key inside.

API Key acquisition links:
- Alibaba Cloud: [https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)
- DeepSeek: [https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)
- GLM: [https://open.bigmodel.cn/](https://open.bigmodel.cn/)

### Running the Application

#### Server

```bash
# server
python ./main.py
```

After startup, the service can be accessed via API.

#### Frontend

The project includes a simple PyWebIO GUI.

```bash
# start frontend service
python ./front.py
```

## Open Source License

This translation is for reference only. In case of any discrepancy, the English version in the LICENSE file shall prevail.

MIT Open Source License:

Copyright (c) 2025 bytesc

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.