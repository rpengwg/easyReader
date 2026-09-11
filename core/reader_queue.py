import queue
import threading


class ReaderQueue:
    def __init__(self, worker):
        self.queue = queue.Queue()
        self.worker = worker
        self.running = False
        self.thread = None
        self.paused = False
        self.lock = threading.Lock()

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def put(self, text, replace=False):
        if not text:
            return
        with self.lock:
            if replace:
                self.clear()
            self.queue.put(text)

    def add(self, text):
        self.put(text)

    def clear(self):
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break

    def stop(self):
        self.running = False
        self.clear()

    def _run(self):
        while self.running:
            try:
                text = self.queue.get(timeout=0.5)
                self.worker(text)
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as exc:
                print(f"ReaderQueue error: {exc}")
