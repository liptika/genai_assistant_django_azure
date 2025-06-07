import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from django.conf import settings
from content_manager.models import UploadedContent
from content_manager.document_utils import extract_text_from_file
from content_manager.azure_search_utils import delete_document

UPLOADS_DIR = os.path.join(settings.MEDIA_ROOT, "uploads")


class UploadsHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        if filename.startswith("~$") or filename.startswith("."):
            print(f"⚠️ Skipping temp/hidden file: {filename}")
            return

        print(f"📥 Detected file: {filename}")
        ext = os.path.splitext(filename)[1].lower()

        try:
            content = extract_text_from_file(event.src_path)

            uploaded = UploadedContent.objects.filter(file__icontains=filename).first()
            if uploaded:
                uploaded.extracted_text = content
                uploaded.save()
                print(f"✅ OCR processed and saved for: {filename}")
            else:
                UploadedContent.objects.create(
                    title=filename,
                    file=os.path.join('uploads', filename),
                    content_type='doc',
                    extracted_text=content,
                )
                print(f"➕ Created new DB record and saved OCR for: {filename}")

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

    def on_deleted(self, event):
        if event.is_directory:
            return

        relative_path = os.path.relpath(event.src_path, settings.MEDIA_ROOT).replace("\\", "/")
        filename = os.path.basename(event.src_path)

        uploaded = UploadedContent.objects.filter(file=relative_path).first()
        if uploaded:
            search_id = uploaded.search_id
            uploaded.delete()
            print(f"🗑️ Deleted DB entry for: {relative_path}")

            if search_id:
                try:
                    delete_document(search_id)
                    print(f"🧹 Removed vectors from Azure AI Search for: {filename}")
                except Exception as e:
                    print(f"⚠️ Failed to delete from Azure Search: {e}")
        else:
            print(f"⚠️ No DB entry found to delete for: {relative_path}")


def start_watching():
    print("👁️ Watching media/uploads for new files...")
    os.makedirs(UPLOADS_DIR, exist_ok=True)

    observer = Observer()
    observer.schedule(UploadsHandler(), path=UPLOADS_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("👋 Watcher stopped.")

    observer.join()
