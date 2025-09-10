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
