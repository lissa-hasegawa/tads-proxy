#Singleton da fila
class RequestQueue:
    _instance = None # Instância única

    def __init__(self):
        if RequestQueue._instance is not None: # verifica se já existe uma instância, para evitar múltiplas instâncias
            raise Exception("Use get_instance()")
        self.queue = [] # inicia a fila com uma lista vazia

    # Método estático para obter a instância única caso já exista, ou criar uma nova
    @staticmethod
    def get_instance():
        if RequestQueue._instance is None:
            RequestQueue._instance = RequestQueue()
        return RequestQueue._instance

    # Adiciona uma requisição ao final da fila
    def enqueue(self, request):
        self.queue.append(request)

    # Retorna todas as requisições na fila
    def get_all(self):
        return self.queue
