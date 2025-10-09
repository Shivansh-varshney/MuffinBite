import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from muffinbite.management.settings import session, BASE_DIR

class ReloadHandler(FileSystemEventHandler):
    """
    Looks out for changes in folders
    """
    def on_created(self, event):
        if not event.is_directory:
            self._handle_change(event, "created")

    def on_modified(self, event):
        if not event.is_directory:
            self._handle_change(event, "modified")

    def on_deleted(self, event):
        if not event.is_directory:
            self._handle_change(event, "deleted")

    def _handle_change(self, event, action):
        if "Attachments" in event.src_path or "DataFiles" in event.src_path:
            session.refresh()

def watch_directories():

    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, str(BASE_DIR / "Attachments"), recursive=False)
    observer.schedule(event_handler, str(BASE_DIR / "DataFiles"), recursive=False)
    observer.start()

def start_watcher():

    thread = threading.Thread(target=watch_directories, daemon=True)

    if (BASE_DIR / "Attachments").exists() and (BASE_DIR / "DataFiles").exists():
        thread.start()