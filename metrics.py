from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry

registry = CollectorRegistry()

queue_size = Gauge('queue_size', 'Tamanho atual da fila', registry=registry)
dropped_requests = Counter('dropped_requests', 'Requisições descartadas', ['reason'], registry=registry)
latency = Histogram('latency_seconds', 'Latência das chamadas ao upstream', registry=registry)
