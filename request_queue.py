class RequestQueue:
    _instance = None

    def __init__(self):
        if RequestQueue._instance is not None:
            raise Exception("Use get_instance()")
        self.queue = []

    @staticmethod
    def get_instance():
        if RequestQueue._instance is None:
            RequestQueue._instance = RequestQueue()
        return RequestQueue._instance

    def enqueue(self, request):
        self.queue.append(request)

    def get_all(self):
        return self.queue
