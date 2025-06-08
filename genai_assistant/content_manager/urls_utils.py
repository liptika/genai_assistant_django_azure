import os
import uuid
import requests
from bs4 import BeautifulSoup
from django.conf import settings

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style tags
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n')
        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        return clean_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def save_text_as_file(text, prefix="scraped_"):
    filename = f"{prefix}{uuid.uuid4().hex}.txt"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Return relative file path for DB storage (so MEDIA_URL + filename works)
    return filename
