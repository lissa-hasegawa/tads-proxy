import requests

def score_cpf(client_id, cpf):
    url = f"https://score.hsborges.dev/api/score?cpf={cpf}" # Exemplo de URL da API ViaCEP

    try:
        resposta = requests.get(url, headers={"client-id": client_id, "accept": "application/json"})
        if resposta.status_code == 200:
            dados = resposta.json()
            print(f"Score: {dados.get('score')}")
        else:
            print(f"Erro ao consultar o CPF. Código de status: {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao fazer a requisição: {e}")


# Exemplo de uso
cpf_para_consultar = "90147174074" # Substitua por um CEP válido
client_id = "1"
score_cpf(client_id, cpf_para_consultar)

