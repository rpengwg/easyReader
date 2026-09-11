import queue
import threading


class ReaderQueue:
    def __init__(self, worker):
        self.queue = queue.Queue()
        self.worker = worker
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()

    def add(self, text):
        self.queue.put(text)

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            try:
                text = self.queue.get(timeout=0.5)
                self.worker(text)
            except queue.Empty:
                continue
