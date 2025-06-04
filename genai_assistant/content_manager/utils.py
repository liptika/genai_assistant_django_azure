#Document Inteligence for Calendar API

import os
import re
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from django.conf import settings

def extract_dates_and_references_from_file(file_path):
    endpoint = settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    key = settings.AZURE_DOCUMENT_INTELLIGENCE_KEY

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(file_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=f)
        result = poller.result()

    content = " ".join([line.content for page in result.pages for line in page.lines])

    # Simple regex to find dates
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\d{4}-\d{2}-\d{2})'
    matches = re.finditer(date_pattern, content)

    events = []
    for match in matches:
        date_text = match.group()
        try:
            # Try parsing to date object
            from dateutil import parser
            date_obj = parser.parse(date_text).date()
            start = max(match.start() - 50, 0)
            end = min(match.end() + 50, len(content))
            context = content[start:end]
            events.append({
                "title": context.strip(),
                "start": str(date_obj)
            })
        except:
            continue

    return events
