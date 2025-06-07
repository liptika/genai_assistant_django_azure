import os
import uuid
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
    HnswParameters,
)
from django.conf import settings

AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE_NAME")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX_NAME")
AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")

def get_index_client():
    endpoint = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"
    return SearchIndexClient(endpoint, AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY))

def get_search_client():
    endpoint = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"
    return SearchClient(endpoint, AZURE_SEARCH_INDEX, AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY))

def ensure_index_exists():
    index_client = get_index_client()
    try:
        index_client.get_index(AZURE_SEARCH_INDEX)
    except:
        index = SearchIndex(
            name=AZURE_SEARCH_INDEX,
            fields=[
                SimpleField(name="id", type="Edm.String", key=True),
                SearchableField(name="title", type="Edm.String"),
                SearchableField(name="content", type="Edm.String"),
                SearchField(
                    name="contentVector",
                    type="Collection(Edm.Single)",  # vector of floats
                    searchable=False,
                    filterable=False,
                    sortable=False,
                    facetable=False,
                    vector_search_dimensions=1536,
                    vector_search_configuration="default",
                ),
            ],
            vector_search=VectorSearch(
                algorithm_configurations=[
                    VectorSearchAlgorithmConfiguration(
                        name="default",
                        kind="hnsw",
                        parameters=HnswParameters(metric="cosine", efConstruction=400, m=4)
                    )
                ]
            ),
        )
        index_client.create_index(index)

def index_document(title, content, vector):
    ensure_index_exists()
    client = get_search_client()
    doc_id = str(uuid.uuid4())
    client.upload_documents([{
        "id": doc_id,
        "title": title,
        "content": content,
        "contentVector": vector
    }])
    return doc_id

def delete_document(doc_id):
    client = get_search_client()
    client.delete_documents(documents=[{"id": doc_id}])
