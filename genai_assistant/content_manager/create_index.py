# content_manager/create_index.py
import os
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
    VectorSearchProfile,
)
from azure.core.credentials import AzureKeyCredential  # Required for authentication
from decouple import config
# Environment variables for configuration
AZURE_SEARCH_SERVICE_NAME = config("AZURE_SEARCH_SERVICE_NAME")
AZURE_SEARCH_API_KEY = config("AZURE_SEARCH_ADMIN_KEY")
AZURE_SEARCH_INDEX_NAME = config("AZURE_SEARCH_INDEX_NAME", "project-doc-index")

def create_or_update_index():
    if not AZURE_SEARCH_SERVICE_NAME or not AZURE_SEARCH_API_KEY:
        print("❌ Azure Search service name or API key environment variables are not set. Cannot create/update index.")
        return

    try:
        search_service_endpoint = f"https://{AZURE_SEARCH_SERVICE_NAME}.search.windows.net"
        index_client = SearchIndexClient(
            endpoint=search_service_endpoint,
            credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
        )

        # 1. Define your vector search algorithm configuration
        vector_search_algorithm_configuration = VectorSearchAlgorithmConfiguration(
            name="my-hnsw-config"
        )
        # Set 'kind' and 'parameters' explicitly (parameters must be a dict)
        vector_search_algorithm_configuration.kind = "hnsw"
        vector_search_algorithm_configuration.parameters = {
            "metric": "cosine",
            "efConstruction": 400,
            "m": 8,
        }

        # 2. Define your vector search profile
        vector_search_profile = VectorSearchProfile(
            name="my-vector-profile",
            algorithm_configuration_name="my-hnsw-config"
        )

        # 3. Combine algorithms and profiles into a VectorSearch object
        vector_search = VectorSearch(
            algorithms=[vector_search_algorithm_configuration],
            profiles=[vector_search_profile]
        )

        # 4. Define your search fields
        fields = [
            SearchField(name="id", type=SearchFieldDataType.String, key=True, searchable=False),
            SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
            SearchField(name="title", type=SearchFieldDataType.String, searchable=True, filterable=True),
            # Vector field linked to the profile
            SearchField(
                name="contentVector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),  # Single == float (correct SDK usage)
                searchable=True,
                vector_search_dimensions=1536,
                vector_search_profile_name="my-vector-profile"
            ),
            # Add more fields as needed
        ]

        # 5. Create the SearchIndex object with fields and vector_search
        index = SearchIndex(
            name=AZURE_SEARCH_INDEX_NAME,
            fields=fields,
            vector_search=vector_search
        )

        print(f"ℹ️ Creating or updating Azure Search index: {AZURE_SEARCH_INDEX_NAME}")
        index_client.create_or_update_index(index)
        print(f"✅ Azure Search index '{AZURE_SEARCH_INDEX_NAME}' created/updated successfully.")

    except Exception as e:
        print(f"❌ Failed to ensure Azure Search index: {e}")
        # Uncomment to debug more deeply:
        # import traceback
        # traceback.print_exc()
