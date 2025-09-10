import time

class RequestIterator:
    def __init__(self, request_queue):
        now = time.time()
        self.queue = [
            req for req in request_queue.get_all()
            if now - req.timestamp <= req.ttl
        ]
        self.queue.sort(key=lambda r: r.priority)

    def __iter__(self):
        return iter(self.queue)
