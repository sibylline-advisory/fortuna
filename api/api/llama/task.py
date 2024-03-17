import logging

from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool, ToolMetadata

from .common import service_context
from .func.currency import send_currency
from .func.db import update_task_with_resolution
from .func.swap import swap_currency

log = logging.getLogger(__name__)

transfer_currency_tool = FunctionTool(
    fn=send_currency,
    metadata=ToolMetadata(
        name="transfer_currency_tool",
        description="Transfers currency to someone or something else, the amount passed to the function must be a "
                    "float, the currency passed to the function must be in ISO 4217 format.",
    )
)

swap_currency_tool = FunctionTool(
    fn=swap_currency,
    metadata=ToolMetadata(
        name="swap_currency_tool",
        description="Swaps an amount of a chosen currency to another currency, the amount passed to the function must "
                    "be a float, the currency passed to the function must be in a crypto ticker format.",
    )
)

update_task_with_resolution = FunctionTool(
    fn=update_task_with_resolution,
    metadata=ToolMetadata(
        name="update_task_with_resolution_tool",
        description="Updates a task with the resolution of said task.",
    )
)

p = """
You are the operations manager of a financial wealth management company. You are to take tasks as directed by 
management from their clients and execute the required financial transactions using the tools provided. You must ensure
that you maintain good record keeping of the tasks with their resolutions.

For example, if a client requests to transfer 1000 USD to a recipient, you must use the transfer_currency_tool to
execute the transaction and then update the task with the resolution of the transaction.

It is essential that the low level call_data necessary to execute the financial transactions on our infrastructure
is passed in valid JSON format to the update_task_with_resolution_tool along with the task id (tid) to update the task.

Each tool will return this call data. Ensure that it is always passed to the update_task_with_resolution_tool in valid
JSON format along with the task id (tid) to update the task.
"""


def get_chat_agent(history=None, callback_manager=None) -> OpenAIAgent:
    agent = OpenAIAgent.from_tools(
        system_prompt=p,
        llm=service_context.llm,
        tools=[transfer_currency_tool, update_task_with_resolution],
        callback_manager=callback_manager,
        verbose=True,
        chat_history=history
    )
    return agent
