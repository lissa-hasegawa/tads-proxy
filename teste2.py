import time
import requests

# 🧱 Classe da Requisição
class ScoreRequest:
    def __init__(self, client_id, cpf, priority=1, ttl=10):
        self.client_id = client_id
        self.cpf = cpf
        self.priority = priority
        self.ttl = ttl
        self.timestamp = time.time()

# 🧱 Singleton da Fila
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

# 🔁 Iterator com Prioridade e TTL
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

# 🚀 Função que envia requisição para a API
def score_cpf(request):
    url = f"https://score.hsborges.dev/api/score?cpf={request.cpf}"
    try:
        resposta = requests.get(url, headers={
            "client-id": request.client_id,
            "accept": "application/json"
        })
        if resposta.status_code == 200:
            dados = resposta.json()
            print(f"[{request.client_id}] CPF: {request.cpf} → Score: {dados.get('score')}")
        else:
            print(f"[{request.client_id}] Erro: {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{request.client_id}] Falha: {e}")

# ⏱️ Scheduler que consome a fila a cada 1 segundo
def scheduler():
    queue = RequestQueue.get_instance()
    while queue.get_all():
        iterator = RequestIterator(queue)
        try:
            request = next(iter(iterator))
            score_cpf(request)
            queue.queue.remove(request)
        except StopIteration:
            print("Nenhuma requisição válida na fila.")
        time.sleep(1)

# 🧪 Simulação com os CPFs fornecidos
def gerar_requisicoes():
    cpfs = [
        "86847277033", "47919572029", "43611951021", "71576542025",
        "37057062095", "73557666000", "50849150000", "00393169049",
        "99814245011", "27399866023", "11111111111"
    ]
    queue = RequestQueue.get_instance()
    for i, cpf in enumerate(cpfs, start=1):
        req = ScoreRequest(client_id=str(i), cpf=cpf, priority=i % 3)
        queue.enqueue(req)
        print(f"Enfileirada: client_id={req.client_id}, cpf={req.cpf}, prioridade={req.priority}")

# 🚦 Execução
if __name__ == "__main__":
    gerar_requisicoes()
    scheduler()
