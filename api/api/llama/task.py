import logging

from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool, ToolMetadata

from .common import service_context
from .func import update_task_with_resolution
from .func.currency import send_currency

log = logging.getLogger(__name__)

transfer_currency_tool = FunctionTool(
    fn=send_currency,
    metadata=ToolMetadata(
        name="Transfer Currency",
        description="Transfers currency to someone or something else.",
    )
)


update_task_with_resolution = FunctionTool(
    fn=update_task_with_resolution,
    metadata=ToolMetadata(
        name="Update Task With Resolution",
        description="Updates a task with the resolution of the task.",
    )
)


def get_chat_agent(history=None, callback_manager=None) -> OpenAIAgent:
    agent = OpenAIAgent.from_tools(
        system_prompt="You are a financial assistant. You are to take identified tasks from your clients, and execute "
                      "them using the tools provided, ensuring you mark the task with the returned value of the tools "
                      "after completion",
        llm=service_context.llm,
        tools=[transfer_currency_tool, update_task_with_resolution],
        callback_manager=callback_manager,
        verbose=True,
        chat_history=history
    )
    return agent
