import time  
import sys
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
from subprocess import Popen, PIPE
import logging
from datetime import datetime


LOGGER = None
PROCESSED_FILES = set()



def config_log():
    global LOGGER
    if not LOGGER:
        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.csv"]

    def process(self, event):
        ROOT = '/home/farma_admin/data/integracao_banco/'

        LOGGER.info('Event identified!')
        if not event.is_directory and event.src_path not in PROCESSED_FILES:
            if 'cadastro_loja/lojas_' in event.src_path:
                LOGGER.info('Event is from cadastro_loja...')
                task = Popen(["/usr/bin/python3", ROOT + "lojas_main.py"], stdout=PIPE, stderr=PIPE)
                LOGGER.info(task)
                PROCESSED_FILES.add(event.src_path)
            elif 'cadastro_produto/produtos_' in event.src_path:
                LOGGER.info('Event is from cadastro_produto')
                task = Popen(["/usr/bin/python3", ROOT + "produtos_main.py"], stdout=PIPE, stderr=PIPE)
                LOGGER.info(task)
                PROCESSED_FILES.add(event.src_path)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)


if __name__ == '__main__':
    config_log()
    LOGGER.info('Initiating configuration...')
    path = '.'
    observer = Observer()
    handler = MyHandler()

    LOGGER.info('Starting observer...')
    observer.schedule(handler, path, recursive=True)
    observer.start()

    LOGGER.info('Listening {}..'.format(path))
    try:
        while True:
            now = datetime.now()
            if now.strftime('%S') == '0':
                PROCESSED_FILES.clear()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()