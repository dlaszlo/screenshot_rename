import logging
import re
import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE_FILE_PATTERN = r"Képernyőkép ekkor: (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})\.png"
DESTINATION_FILE_PATTERN = "screenshot_%Y-%m-%d_%H-%M-%S.png"
SCREENSHOT_PATH = "/screenshots"

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger("auto_rename")


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        try:
            file_path = event.src_path
            match = re.search(SOURCE_FILE_PATTERN,
                              os.path.basename(file_path))
            if match:
                date_str = match.group(1)
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H-%M-%S")
                new_filename = date_obj.strftime(DESTINATION_FILE_PATTERN)
                new_path = os.path.join(os.path.dirname(file_path), new_filename)
                logger.info(f'Rename: {os.path.basename(file_path)} -> {new_filename}')
                os.rename(file_path, new_path)
        except Exception as e:
            logger.error("Error occurred", e)


if __name__ == "__main__":

    logger.info(f"Path: {SCREENSHOT_PATH}")

    event_handler = EventHandler()

    observer = Observer()
    observer.schedule(event_handler, SCREENSHOT_PATH, recursive=True)

    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
