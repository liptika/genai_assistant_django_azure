from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import AzureChatOpenAI
from django.conf import settings

global_memory = ConversationBufferMemory(return_messages=True)

def get_langchain_chain():
    llm = AzureChatOpenAI(
        openai_api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        deployment_name=settings.AZURE_OPENAI_DEPLOYMENT,
        openai_api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.7,
        max_tokens=500
    )

    return ConversationChain(
        llm=llm,
        memory=global_memory,
        verbose=True,
    )
