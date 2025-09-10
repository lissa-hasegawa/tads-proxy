import time
import requests
from request_queue import RequestQueue
from iterator import RequestIterator
from metrics import queue_size, latency

def score_cpf(request):
    url = f"https://score.hsborges.dev/api/score?cpf={request.cpf}"
    start = time.time()
    try:
        resposta = requests.get(url, headers={
            "client-id": request.client_id,
            "accept": "application/json"
        })
        duration = time.time() - start
        latency.observe(duration)
        if resposta.status_code == 200:
            dados = resposta.json()
            print(f"[{request.client_id}] CPF: {request.cpf} → Score: {dados.get('score')}")
        else:
            print(f"[{request.client_id}] Erro: {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{request.client_id}] Falha: {e}")

def start_scheduler():
    queue = RequestQueue.get_instance()
    while True:
        queue_size.set(len(queue.get_all()))
        iterator = RequestIterator(queue)
        try:
            request = next(iter(iterator))
            score_cpf(request)
            queue.queue.remove(request)
        except StopIteration:
            pass
        time.sleep(1)
