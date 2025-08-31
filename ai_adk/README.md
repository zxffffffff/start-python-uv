# ai-adk

使用 Google ADK 框架开发 AI 工作流。

## 框架说明

Agent Development Kit (ADK) 是一个灵活的模块化框架，用于开发和部署 AI 代理 。ADK 针对 Gemini 和 Google 生态系统进行了优化，同时具备模型无关性和部署无关性 ，并且专为以下目的构建： 与其他框架的兼容性 。ADK 的设计初衷是让代理开发更像软件开发，让开发人员能够更轻松地创建、部署和协调从简单任务到复杂工作流的代理架构。

### 命令说明

用法: adk api_server [OPTIONS] [AGENTS_DIR]

为 agents 启动一个 FastAPI 服务器。

AGENTS_DIR: agents 的目录，其中每个子目录都是一个单独的 agent，至少包含 `__init__.py` 和 `agent.py` 文件。

示例:

adk api_server --port=[port] path/to/agents_dir

### 启动服务

```shell
uv run adk web --host 0.0.0.0 --port 5003 --log_level DEBUG --reload_agents
```
