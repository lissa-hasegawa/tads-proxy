# Lidando com rate limiting

Desafio da Disciplina de Técnicas Avançadas em Desenvolvimento de Software com o objetivo de criar um serviço de proxy interno para consumir a API pública de uma empresa parceira disponível em https://score.hsborges.dev/docs.

## Missão ✅

Projetar e entregar um serviço proxy com:

1. **Fila/Buffer interno** para lidar com picos (backpressure);
2. **Scheduler** para emitir no **máximo 1 chamada/segundo** ao upstream;
3. **Política de enfileiramento** configurável (ex.: FIFO, prioridade por tipo de operação, deadline/TTL);
4. **Estratégia de degradação** (fallback) quando a fila cresce demais (ex.: shed load, respostas cacheadas, etc);
5. **Observabilidade**: logs estruturados, métricas (contadores, histograma de latência, taxa de erro, tamanho da fila), e dashboard simples;
6. **Configurações** (via arquivo/env): limites, tamanhos de fila, timeouts, política de retry;

## Arquitetura 🖇️

Para este desafio, foi adotado os seguintes padrões de projeto:

- **_Singleton_** é uma abordagem de design que garante que uma classe tenha apenas uma instância durante todo o ciclo de vida da aplicação, e fornece um ponto global de acesso a essa instância. Dessa forma, evitar múltiplas instâncias de um serviço, recurso compartilhado ou fila, o que poderia causar inconsistências ou sobrecarga.
- **_Iterator_** permite percorrer uma coleção de elementos (como uma fila de requisições) sem expor sua estrutura interna. Portanto, facilita a navegação sequencial sobre os itens de uma coleção, como uma fila, lista ou conjunto.

- **_Flask_** é um microframework web escrito em Python oferecendo apenas os componentes essenciais para construir aplicações web fazendo o mínimo necessário, e permitindo que o desenvolvedor adicione apenas o que precisa. Possui mais simplicidade, flexibilidade, extensibilidade, curva de aprendizado fácil, síncrono por padrão, além de possuir um controle manual.

## ⚙️ Execução do sistema

Rodar `app.py` em terminal separado

**Motivo:**  
O arquivo `app.py` inicia o servidor Flask e o scheduler em uma thread paralela. Para que o sistema funcione corretamente e aceite requisições externas, ele deve ser executado em um terminal dedicado, mantendo o processo ativo e escutando na porta `5000`.

```bash
python app.py
```

> ⚠️ Importante: rodar `app.py` no mesmo terminal que executa os testes pode interromper o servidor ou impedir que o scheduler funcione corretamente.

---

## 🧪 Experimento: execução de `teste_proxy.py`

O script `teste_proxy.py` foi utilizado para enviar 10 requisições simultâneas para o endpoint `/proxy/score`, cada uma com um CPF diferente e um `client-id` único.

```bash
python teste_proxy.py
```

### 📤 Saída no terminal `teste_proxy.py`

```
[3] CPF: 43611951021
[4] CPF: 71576542025
[5] CPF: 37057062095
[8] CPF: 00393169049
[1] CPF: 86847277033
[10] CPF: 27399866023
[9] CPF: 99814245011
[2] CPF: 47919572029
[6] CPF: 73557666000
[7] CPF: 50849150000
```
> As requisições são enfileiradas com sucesso, mas o script não aguarda nem exibe o resultado final dos scores.

---

### 📥 Saída no terminal `app.py`

```
127.0.0.1 - - [28/Sep/2025 14:06:51] "GET /proxy/score?cpf=..." 200 -
...
[3] CPF: 43611951021 → Score: 165
[4] CPF: 71576542025 → Score: 231
[5] CPF: 37057062095 → Score: 275
[8] CPF: 00393169049 → Score: 319
[1] CPF: 86847277033 → Score: 275
[10] CPF: 27399866023 → Score: 297
[9] CPF: 99814245011 → Score: 176
[2] CPF: 47919572029 → Score: 308
[6] CPF: 73557666000 → Score: 209
[7] CPF: 50849150000 → Score: 131
```

> O scheduler processa uma requisição por segundo, respeitando o rate limit e exibindo os scores no terminal.


## 🧠 Análise técnica e trade-offs

### ✅ Arquitetura mantida
- Fila de requisições com padrão Singleton
- Prioridade e TTL para controle de expiração
- Scheduler assíncrono com processamento a cada 1 segundo
- Rate limit garantido sem sobrecarga da API externa

### ⚖️ Trade-offs 

#### Enfileiramento assíncrono vs. resposta imediata
- **Escolha:** Requisições são enfileiradas e processadas posteriormente.
- **Vantagem:** Protege a API externa, permite priorização e controle de carga.
- **Desvantagem:** O cliente não recebe o score imediatamente; `teste_proxy.py` não exibe o resultado final.

#### TTL fixo vs. adaptabilidade
- **Escolha:** TTL estático para cada requisição.
- **Vantagem:** Fácil de implementar e entender.
- **Desvantagem:** Requisições podem expirar mesmo sendo válidas, se a fila estiver cheia.

---

## ✅ Conclusão

Apesar de ter sido considerado um código síncrono que retornaria o resultado na hora para o cliente, isso afetaria o padrão de enfileiramento e controle de taxa, além de não respeitar TTL nem prioridade. Então o código síncrono foi descartado e foi mantido o formato inicial, o que faz com que o score do CPF não seja visíve no terminal de `teste_proxy.py`, apenas em `app.py`.

- As requisições foram enfileiradas e são processadas corretamente
- O rate limit de 1 requisição/segundo foi respeitado
- TTL e prioridade são respeitados
- O cliente não aguarda o resultado, mas o processamento é visível no terminal do servidor

