
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
   cd genai_assistant_django_azure
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
4. **Go inside Django Project to run and set environments variables**
   ```bash
   cd genai_assistant
5. **Configure environment variables**
    ```python
    AZURE_OPENAI_KEY = "your_openai_key"
    AZURE_OPENAI_ENDPOINT = "https://your-endpoint.openai.azure.com/"
    AZURE_OPENAI_DEPLOYMENT_NAME = "your_deployment_name"

    AZURE_DOCUMENT_INTELLIGENCE_KEY = "your_doc_intelligence_key"
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://your-docintelligence-endpoint/"
    
    AZURE_AI_SEARCH_KEY = "your_ai_search_key"
    AZURE_AI_SEARCH_ENDPOINT = "https://your-aisearch-endpoint/"

    OPENWEATHER_API_KEY = "your_openweather_api_key"
6. **Apply database migrations**
    ```python
    python manage.py makemigrations
    python manage.py migrate
7. **Run the development server**
    ```python
    python manage.py runserver
8. **Access the application**
    ```cpp
    http://127.0.0.1:8000/

---

## 📂 Project Structure
```bash
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
```

---

## ✅ Pages and Routes
| Page             | URL                  | Description                                 |
| :--------------- | :------------------- | :------------------------------------------ |
| Home             | `/`                  | Central hub with upload, calendar, and chat |
| Upload           | `/upload/`           | Upload content for analysis                 |
| Explore          | `/explore/`          | Ask general queries (no file context)       |
| Time Map         | `/calendar-test/`    | A detailed calendar view with categories    |
| Uploaded Content | `/content_list/`     | List of uploaded files                      |
| Saved Chats      | `/saved-chats/`      | View previous conversations                 |

---

## 📸 Screenshots
---
![AskEra Home](/images/Home.PNG "Welcome to AskEra")

---

## 📄 License
```markdown
- This project is licensed under the [MIT License](/LICENSE).

---
## Contact
```markdown
- **Liptika Dhal**  
[GitHub](https://github.com/liptika) • [LinkedIn](https://linkedin.com/in/liptikadhal)

## 🚀 Future Scope

AskEra is designed with extensibility in mind. Here are some planned or possible future enhancements:

- **🔎 Grounded AI Agents with Bing Search**: Integrate Azure AI Agents and Grounding with Bing Search to provide more factual, real-time, and context-aware responses for complex queries.

- **📌 Persistent User Profiles**: Implement user login and personalized dashboards to allow saved preferences, tracked learning history, and content tagging.

- **🗣️ Voice Input & Output**: Enable voice-based interactions with speech-to-text and text-to-speech capabilities, making AskEra more accessible and interactive.

- **🌐 Multi-language Support**: Expand support to regional and global languages to serve a more diverse audience.

- **📥 Enhanced File Handling**: Add support for ZIP and Markdown formats with richer content parsing and summarization features.

- **📡 Real-time Collaboration**: Enable multiple users to annotate and discuss uploaded documents simultaneously, useful for knowledge gathering or research.

- **🔐 OAuth2 Integration**: Add secure login via Google, Microsoft, or GitHub for user-specific content tracking.

---

These additions aim to make AskEra not just an assistant, but a dynamic, intelligent learning companion.








