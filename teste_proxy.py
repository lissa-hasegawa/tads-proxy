import requests
from concurrent.futures import ThreadPoolExecutor

# Lista de CPFs para teste
cpfs = [
    "86847277033", "47919572029", "43611951021", "71576542025",
    "37057062095", "73557666000", "50849150000", "00393169049",
    "99814245011", "27399866023"
]

# Função que envia uma requisição para o proxy
def send_request(i, cpf):
    url = f"http://localhost:5000/proxy/score?cpf={cpf}"
    headers = {"client-id": str(i)}
    try:
        response = requests.get(url, headers=headers)

        print(f"[{i}] CPF: {cpf}")

    except Exception as e:
        print(f"[{i}] CPF: {cpf} → Erro: {e}")

from concurrent.futures import ThreadPoolExecutor, as_completed

futures = []
with ThreadPoolExecutor(max_workers=len(cpfs)) as executor:
    for i, cpf in enumerate(cpfs, start=1):
        futures.append(executor.submit(send_request, i, cpf))

for future in as_completed(futures):
    future.result()
