#!/usr/bin/env python
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, RegexMatchingEventHandler

class MyEventHandler(PatternMatchingEventHandler, LoggingEventHandler):
	pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'data'
    patterns = ['*.csv.gz']
    event_handler = MyEventHandler(patterns, case_sensitive=True)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
