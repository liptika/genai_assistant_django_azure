
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import AzureChatOpenAI
from django.conf import settings

import os
from typing import List

from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import AIMessage

from langchain_openai import AzureOpenAIEmbeddings
from content_manager.azure_search_utils import get_search_client
from azure.search.documents.models import VectorizedQuery

from decouple import config

global_memory = ConversationBufferMemory(return_messages=True)

def get_langchain_chain_updated():
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


# Embedding model setup
embedding_model = AzureOpenAIEmbeddings(
    api_key=config("AZURE_OPENAI_EMBEDDING_API_KEY", settings.AZURE_OPENAI_EMBEDDING_API_KEY),
    azure_endpoint=config("AZURE_OPENAI_EMBEDDING_ENDPOINT", settings.AZURE_OPENAI_EMBEDDING_ENDPOINT),
    azure_deployment=config("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT),
    api_version=config("AZURE_OPENAI_EMBEDDING_API_VERSION", settings.AZURE_OPENAI_EMBEDDING_API_VERSION),
)

def embed_text(text: str) -> List[float]:
    return embedding_model.embed_query(text)

def embed_texts(texts: List[str]) -> List[List[float]]:
    return embedding_model.embed_documents(texts)

def split_text_to_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)

def search_azure_ai(query: str, k: int = 3) -> List[str]:
    vector = embed_text(query)
    search_client = get_search_client()
    print(f"Search client type: {type(search_client)}") #for debugging

    try:
        results = search_client.search(
            search_text="",  # Required but unused when doing vector search
            vector_queries=[
                VectorizedQuery(
                    vector=vector,
                    fields="contentVector"
                )
            ],
            select=["content", "title"],
            top=k  # Pass 'k' using 'top'
        )
        documents = [doc["content"] for doc in results]
        return documents
    except Exception as e:
        print(f"Azure AI Search query failed: {e}")
        return []

def get_langchain_chain():
    """
    Custom RAG chain using manual Azure Cognitive Search and AzureChatOpenAI.
    """
    llm = AzureChatOpenAI(
        api_key=config("AZURE_OPENAI_API_KEY", settings.AZURE_OPENAI_API_KEY),
        azure_endpoint=config("AZURE_OPENAI_ENDPOINT", settings.AZURE_OPENAI_ENDPOINT),
        azure_deployment=config("AZURE_OPENAI_DEPLOYMENT", settings.AZURE_OPENAI_DEPLOYMENT),
        api_version=config("AZURE_OPENAI_API_VERSION", settings.AZURE_OPENAI_API_VERSION),
        temperature=0.7,
        max_tokens=500,
    )

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful assistant. Use the context below to answer the user's question.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:
""",
    )

    def rag_chain(question: str):
        context_docs = search_azure_ai(question)
        context = "\n\n".join(context_docs) if context_docs else "No relevant documents found."
        final_prompt = prompt_template.format(context=context, question=question)
        response = llm.invoke(final_prompt)
        return response.content if isinstance(response, AIMessage) else str(response)

    return rag_chain


# ✅ New function: Generate AI summary from full Azure AI Search context
def generate_ai_summary(prompt: str) -> str:
    llm = AzureChatOpenAI(
        api_key=config("AZURE_OPENAI_API_KEY", settings.AZURE_OPENAI_API_KEY),
        azure_endpoint=config("AZURE_OPENAI_ENDPOINT", settings.AZURE_OPENAI_ENDPOINT),
        azure_deployment=config("AZURE_OPENAI_DEPLOYMENT", settings.AZURE_OPENAI_DEPLOYMENT),
        api_version=config("AZURE_OPENAI_API_VERSION", settings.AZURE_OPENAI_API_VERSION),
        temperature=0.5,
        max_tokens=700,
    )

    # Pull top 10 relevant chunks (more context for summary)
    documents = search_azure_ai(prompt, k=10)
    context = "\n\n".join(documents) if documents else "No relevant content available."

    full_prompt = f"""You are a summarizer. Based on the following content, respond to the prompt: "{prompt}"

Content:
{context}

Summary:"""

    response = llm.invoke(full_prompt)
    return response.content if isinstance(response, AIMessage) else str(response)