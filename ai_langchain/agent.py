import json
import time
from dotenv import load_dotenv
from typing import (
    Annotated,
    Sequence,
    TypedDict,
)
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool, BaseTool
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from IPython.display import Image, display

best_model = "qwen-max"  # 适合复杂任务，能力最强（128K）
fast_model = "qwen-turbo"  # 适合简单任务，速度快、成本极低（1M）
long_model = "qwen-long"  # 适合大规模文本分析，效果与速度均衡、成本较低（10M）

# 加载 .env 文件
load_dotenv()


class AgentState(TypedDict):
    """The state of the agent."""

    # add_messages is a reducer
    # See https://langchain-ai.github.io/langgraph/concepts/low_level/#reducers
    messages: Annotated[Sequence[BaseMessage], add_messages]


class ReActAgent:
    def __init__(
        self,
        model_name=fast_model,
        prompt="You are a helpful AI assistant, please respond to the users query to the best of your ability!",
    ):
        self.model_name = model_name
        self.prompt = prompt
        self.model = None
        self.tools = []
        self.tools_by_name = []
        self.graph = None

    def set_model_name(self, model_name):
        self.model_name = model_name

    def set_prompt(self, prompt):
        self.prompt = prompt

    def add_tool_func(self, tool_func):
        assert isinstance(tool_func, BaseTool)
        self.tools.append(tool_func)

    def add_func(self, func):
        assert callable(func) and hasattr(func, "__name__") and hasattr(func, "__doc__")
        tool_func = tool(func)
        self.add_tool_func(tool_func)

    def clear_tools(self):
        self.tools = []

    def compile(self, display_graph=False):
        self.model = ChatTongyi(model=self.model_name)
        self.tools_by_name = []
        if len(self.tools) > 0:
            self.model = self.model.bind_tools(self.tools)
            self.tools_by_name = {tool.name: tool for tool in self.tools}
            print("---------------- tools ----------------")
            for tool_func in self.tools:
                print(tool_func.name, tool_func.description.replace("\n\n", "\n"))
                print("---------------------------------------")

        # Define our tool node
        def tool_node(state: AgentState):
            outputs = []
            for tool_call in state["messages"][-1].tool_calls:
                tool_result = self.tools_by_name[tool_call["name"]].invoke(
                    tool_call["args"]
                )
                outputs.append(
                    ToolMessage(
                        content=json.dumps(tool_result),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )
            return {"messages": outputs}

        # Define the node that calls the model
        def call_model(
            state: AgentState,
            config: RunnableConfig,
        ):
            # this is similar to customizing the create_react_agent with 'prompt' parameter, but is more flexible
            system_prompt = SystemMessage(self.prompt)
            response = self.model.invoke([system_prompt] + state["messages"], config)
            # We return a list, because this will get added to the existing list
            return {"messages": [response]}

        # Define the conditional edge that determines whether to continue or not
        def should_continue(state: AgentState):
            messages = state["messages"]
            last_message = messages[-1]
            # If there is no function call, then we finish
            if not last_message.tool_calls:
                return "end"
            # Otherwise if there is, we continue
            else:
                return "continue"

        # Define a new graph
        workflow = StateGraph(AgentState)

        # Define the two nodes we will cycle between
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.set_entry_point("agent")

        # We now add a conditional edge
        workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            should_continue,
            # Finally we pass in a mapping.
            # The keys are strings, and the values are other nodes.
            # END is a special node marking that the graph should finish.
            # What will happen is we will call `should_continue`, and then the output of that
            # will be matched against the keys in this mapping.
            # Based on which one it matches, that node will then be called.
            {
                # If `tools`, then we call the tool node.
                "continue": "tools",
                # Otherwise we finish.
                "end": END,
            },
        )

        # We now add a normal edge from `tools` to `agent`.
        # This means that after `tools` is called, `agent` node is called next.
        workflow.add_edge("tools", "agent")

        # Now we can compile and visualize our graph
        self.graph = workflow.compile()

        if display_graph:
            try:
                display(Image(self.graph.get_graph().draw_mermaid_png()))
            except Exception:
                # This requires some extra dependencies and is optional
                pass

    def invoke(self, user_input: str):
        inputs = {"messages": [("user", user_input)]}
        stream = self.graph.stream(inputs, stream_mode="values")

        start_time = time.time()
        message = None
        response = None
        for s in stream:
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
                response = str(message)
            else:
                message.pretty_print()
                response = message.content

        end_time = time.time()
        use_sec = end_time - start_time
        print(f"agent invoke 耗时={use_sec:.2f}秒 {message}", flush=True)
        return response


@tool
def get_weather(location: str):
    """Call to get the weather from a specific location."""
    # This is a placeholder for the actual implementation
    # Don't let the LLM know this though 😊
    if any([city in location.lower() for city in ["sf", "san francisco"]]):
        return "It's sunny in San Francisco, but you better look out if you're a Gemini 😈."
    else:
        return f"I am not sure what the weather is in {location}"


if __name__ == "__main__":
    agent = ReActAgent()
    agent.add_tool_func(get_weather)
    agent.compile(display_graph=True)

    print("输入 'q' 结束对话", flush=True)
    while True:
        txt = input("\n输入: ")
        """
        获取 san francisco 和 new york 的天气，以 JSON 格式返回 {"location":"weather"}
        """
        if txt.lower() == "q":
            break
        if txt.strip() == "":
            continue
        print(flush=True)
        agent.invoke(txt)
