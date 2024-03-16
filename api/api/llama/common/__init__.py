import openai
from llama_index.core.service_context import ServiceContext
from llama_index.embeddings.openai import OpenAIEmbedding
import logging

from llama_index.llms.openai import OpenAI

from ...settings import secure_settings


log = logging.getLogger(__name__)


openai.api_key = secure_settings.openai_key

embed_model = OpenAIEmbedding(embed_batch_size=10, api_key=secure_settings.openai_key)
llm = OpenAI(model="gpt-4-1106-preview")

service_context = ServiceContext.from_defaults(embed_model=embed_model,
                                               chunk_size=512,
                                               llm=llm)
