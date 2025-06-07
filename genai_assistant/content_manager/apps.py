from django.apps import AppConfig
import threading
import os


class ContentManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "content_manager"

    def ready(self):
        # Prevent duplicate execution in Django dev server
        if os.environ.get('RUN_MAIN') != 'true':
            return

        # 🔹 Ensure Azure Search Index Exists
        try:
            from .create_index import create_or_update_index
            create_or_update_index()
        except Exception as e:
            print(f"❌ Failed to ensure Azure Search index: {e}")

        # 🔹 Start File Watcher Thread
        try:
            from .file_watcher import start_watching
            thread = threading.Thread(target=start_watching, daemon=True)
            thread.start()
        except Exception as e:
            print(f"❌ Failed to start file watcher: {e}")

