import threading
import time

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def run(self):
        raise Exception('nip')

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()



class MyTask(StoppableThread):
    def run(self):
        while not self.stopped():
            time.sleep(1)
            print("Hello")

def test():
    testthread = MyTask()
    testthread.start()
    time.sleep(5)
    testthread.stop()
