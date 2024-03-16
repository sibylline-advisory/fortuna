import logging

from llama_index.agent.openai import OpenAIAgent

from .common import service_context

log = logging.getLogger(__name__)


def get_chat_agent(history=None, callback_manager=None) -> OpenAIAgent:
    agent = OpenAIAgent.from_tools(
        system_prompt="",  # TODO: add system prompt
        llm=service_context.llm,
        tools=[],
        callback_manager=callback_manager,
        verbose=True,
        chat_history=history
    )
    return agent
