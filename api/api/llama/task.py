import logging

from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool, ToolMetadata

from .common import service_context
from .func.db import update_task_with_resolution
from .func.currency import send_currency

log = logging.getLogger(__name__)

transfer_currency_tool = FunctionTool(
    fn=send_currency,
    metadata=ToolMetadata(
        name="transfer_currency_tool",
        description="Transfers currency to someone or something else, the amount passed to the function must be a "
                    "float, the currency passed to the function must be in ISO 4217 format.",
    )
)


update_task_with_resolution = FunctionTool(
    fn=update_task_with_resolution,
    metadata=ToolMetadata(
        name="update_task_with_resolution_tool",
        description="Updates a task with the resolution of said task.",
    )
)


def get_chat_agent(history=None, callback_manager=None) -> OpenAIAgent:
    agent = OpenAIAgent.from_tools(
        system_prompt="You are a financial assistant. You are to take identified tasks from your clients, and execute "
                      "them using the tools provided, you must ensure after you have finished executing a task that you "
                      "update said task with exact response (resolution) of previous tools used.",
        llm=service_context.llm,
        tools=[transfer_currency_tool, update_task_with_resolution],
        callback_manager=callback_manager,
        verbose=True,
        chat_history=history
    )
    return agent
