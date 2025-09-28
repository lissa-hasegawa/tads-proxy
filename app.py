from flask import Flask, request, jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from request_queue import RequestQueue
from request_model import ScoreRequest
from scheduler import start_scheduler
import threading
import time
import requests
# o que é threading? 
# É uma biblioteca padrão do Python que permite a execução de múltiplas threads (linhas de execução) dentro de um mesmo processo. 
app = Flask(__name__)
queue = RequestQueue.get_instance() # Obtém a instância única da fila de requisições

# Cria uma thread paralela que roda o start_scheduler()
# daemon=True faz com que a thread seja encerrada quando o programa principal terminar
threading.Thread(target=start_scheduler, daemon=True).start()

@app.route("/proxy/score", methods=["GET"])
def proxy_score():
    client_id = request.headers.get("client-id")
    cpf = request.args.get("cpf")

    if not client_id or not cpf:
        return jsonify({"error": "client-id e cpf são obrigatórios"}), 400
    
    req = ScoreRequest(client_id=client_id, cpf=cpf)
    queue.enqueue(req)
    return jsonify({"status": "enfileirada", "cpf": cpf, "client_id": client_id})

@app.route("/metrics", methods=["GET"])
def metrics():
    from metrics import registry
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Serviço ativo"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
