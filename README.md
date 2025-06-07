
# AskEra: Your AI Companion 🤖📚

AskEra is a personalized AI assistant powered by Azure and OpenAI, built with Django. It enables users to interact with their own documents through natural language, generate flashcards, extract dates for calendar integration, and explore general queries—all in one elegant interface.

---

## 🚀 Features

- 🧠 **Chatbot Integration** – Chat with your documents using Azure OpenAI & Langchain.
- 📁 **File Upload** – Supports `.pdf`, `.txt`, `.xlsx`, `.ppt`, `.jpg`, `.doc`.
- 🗂️ **Manage Uploaded Content** – View and delete uploaded files based on file name and upload time.
- ⛅ **Weather API Integration** – Get real-time weather updates based on your current location.
- 🗂️ **Content Understanding** – Analyze documents using Azure Document Intelligence.
- 📅 **Calendar Extraction** – Automatically pull dates & events into a visual calendar with personal sphere and professional sphere seperated.
- 🧾 **Flashcard Generation** – Learn quickly with AI-generated flashcards to monitor pending work items and to predict upcoming workloads.
- 🔍 **Explore Page** – Ask open-ended questions using only OpenAI (no document context).


---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **AI Services**: Azure OpenAI, Azure Document Intelligence, Azure AI Search
- **Weather API**: OpenWeatherMap API
- **AI Toolkits**: Langchain, Azure OpenAI Embeddings
- **Frontend**: HTML, Bootstrap, JavaScript, [FullCalendar](https://fullcalendar.io/)
- **Storage**: Local filesystem for uploads, Azure AI Search for vector


---

## 🌐 Azure Services Used

- 🔹 Azure OpenAI (chat and embeddings)
- 🔹 Azure Document Intelligence (for document parsing)
- 🔹 Azure AI Search (Vector storing)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/liptika/genai_assistant_django_azure.git
   cd genai_assistant
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
3. **Install dependencies**
   pip install -r requirements.txt
4. **Configure environment variables**
    AZURE_OPENAI_KEY = "your_openai_key"
    AZURE_OPENAI_ENDPOINT = "https://your-endpoint.openai.azure.com/"
    AZURE_OPENAI_DEPLOYMENT_NAME = "your_deployment_name"

    AZURE_DOCUMENT_INTELLIGENCE_KEY = "your_doc_intelligence_key"
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://your-docintelligence-endpoint/"
    
    AZURE_AI_SEARCH_KEY = "your_ai_search_key"
    AZURE_AI_SEARCH_ENDPOINT = "https://your-aisearch-endpoint/"

    OPENWEATHER_API_KEY = "your_openweather_api_key"
5. **Apply database migrations**
    python manage.py makemigrations
    python manage.py migrate
6. **Run the development server**
    python manage.py runserver
7. **Access the application**
    http://127.0.0.1:8000/

---

## 📂 Project Structure

genai_assistant/
│
├── content_manager/          # Main Django app
│ ├── views.py                # All major views and logic
│ ├── models.py               # Models for files, chats, etc.
│ ├── urls.py                 # URL routing
│ ├── utils.py                # date extraction helpers
│ ├── other utlils ...        # Azure/OpenAI/date extraction helpers
│ ├── templates/
│ │ └── content_manager/
│ │ ├── home.html             # Homepage with chat, calendar, upload
│ │ ├── explore.html          # Explore page for general queries
│ │ └── ...                   # Other templates
│                  
├── media/                    # Uploaded files (PDFs, PPTs, etc.)
├── db.sqlite3                # SQLite database (using locally)
├── manage.py
└── requirements.txt

