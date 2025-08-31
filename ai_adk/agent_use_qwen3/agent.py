import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# 通义千问系列
qwen_models = [
    # Max 效果最好的模型，适合复杂、多步骤的任务。
    "qwen-max-latest",
    "qwen-max",
    "qwen-max-2025-01-25",
    # Plus 能力均衡，适合中等复杂任务。
    "qwen-plus-latest",
    "qwen-plus",
    "qwen-plus-2025-07-28",
    "qwen-plus-2025-07-14",
    "qwen-plus-2025-04-28",
    # Flash 通义千问系列速度最快、成本极低的模型，适合简单任务。
    "qwen-flash",
    "qwen-flash-2025-07-28",
    # Turbo 不再更新，建议替换为通义千问Flash。
    "qwen-turbo-latest",
    "qwen-turbo",
    "qwen-turbo-2025-07-15",
    "qwen-turbo-2025-04-28",
    "qwen-turbo-2025-02-11",
    # Long 上下文窗口最长，能力均衡且成本较低的模型，适合长文本分析、信息抽取、总结摘要和分类打标等任务。
    "qwen-long-latest",
    "qwen-long",
    "qwen-long-2025-01-25",
]

best_model = "qwen-max"  # 适合复杂任务，能力最强（128K）
fast_model = "qwen-turbo"  # 适合简单任务，速度快、成本极低（1M）
long_model = "qwen-long"  # 适合大规模文本分析，效果与速度均衡、成本较低（10M）


def get_weather(city: str) -> dict:
    """获取指定城市的当前天气预报。

    Args:
        city (str): 要获取天气预报的城市名称。

    Returns:
        dict: 状态和结果或错误消息。
    """
    if city.lower() == "深圳":
        return {
            "status": "success",
            "report": ("深圳的天气晴，气温为 25 摄氏度。"),
        }
    else:
        return {
            "status": "error",
            "error_message": f"无法获取 '{city}' 的天气信息。",
        }


def get_current_time(city: str) -> dict:
    """返回指定城市当前的时间。

    Args:
        city (str): 用于获取指定城市当前时间的名称。

    Returns:
        dict: 状态和结果或错误消息。
    """

    if city.lower() == "深圳":
        tz_identifier = "Asia/Shanghai"
    else:
        return {
            "status": "error",
            "error_message": (f"无法获取 '{city}' 的时间信息。"),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f"当前 {city} 的时间是 {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(model=f"openai/{best_model}"),
    description=("负责回答有关某一城市的时间和天气情况的问题的 Agent"),
    instruction=(
        "你是一名乐于助人的客服人员，能够回答用户关于某个城市的时间和天气的相关问题。"
    ),
    tools=[get_weather, get_current_time],
)
