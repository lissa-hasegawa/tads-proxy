import time

class ScoreRequest:
    def __init__(self, client_id, cpf, priority=1, ttl=30):
        self.client_id = client_id
        self.cpf = cpf
        self.priority = priority
        self.ttl = ttl
        self.timestamp = time.time()
