import time  
import sys
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
import logging


LOGGER = None


def config_log():
    global LOGGER
    if not LOGGER:
        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*"]

    def process(self, event):
        #DO LOGIC HERE
        LOGGER.info(event)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)


if __name__ == '__main__':
    config_log()

    LOGGER.info('Initiating configuration...')
    path = './input'
    observer = Observer()
    handler = MyHandler()

    LOGGER.info('Starting observer...')
    observer.schedule(handler, path, recursive=True)
    observer.start()

    LOGGER.info('Listening {}..'.format(path))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()