# Requires:
#
# watchdog

import time
from datetime import datetime

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


PROCESSED_FILES = set()


class HotfolderHandler(PatternMatchingEventHandler):
    patterns = ["*.csv"]

    def process(self, event):
        print('Event identified!')
        if not event.is_directory and event.src_path not in PROCESSED_FILES:
            # Do logic...
            print(event.src_path)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

# This also counts with a duplication safe strategy
if __name__ == '__main__':
    print('Initiating configuration...')
    path = '.'
    observer = Observer()
    handler = HotfolderHandler()

    print('Starting observer...')
    observer.schedule(handler, path, recursive=True)
    observer.start()

    print('Listening {}..'.format(path))
    try:
        while True:
            now = datetime.now()
            if now.strftime('%S') == '0':
                PROCESSED_FILES.clear()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
