# Lidando com rate limiting

Desafio da Disciplina de Técnicas Avançadas em Desenvolvimento de Software com o objetivo de criar um serviço de proxy interno para consumir a API pública de uma empresa parceira disponível em https://score.hsborges.dev/docs.

## Missão

Projetar e entregar um serviço proxy com:

1. _Fila/Buffer interno_ para lidar com picos (backpressure);
2. _Scheduler_ para emitir no _máximo 1 chamada/segundo_ ao upstream;
3. _Política de enfileiramento_ configurável (ex.: FIFO, prioridade por tipo de operação, deadline/TTL);
4. _Estratégia de degradação_ (fallback) quando a fila cresce demais (ex.: shed load, respostas cacheadas, etc);
5. _Observabilidade_: logs estruturados, métricas (contadores, histograma de latência, taxa de erro, tamanho da fila), e dashboard simples;
6. _Configurações_ (via arquivo/env): limites, tamanhos de fila, timeouts, política de retry;

## Arquitetura

Para este desafio, foi adotado os seguintes padrões de projeto:

- _Singleton_ é uma abordagem de design que garante que uma classe tenha apenas uma instância durante todo o ciclo de vida da aplicação, e fornece um ponto global de acesso a essa instância. Dessa forma, evitar múltiplas instâncias de um serviço, recurso compartilhado ou fila, o que poderia causar inconsistências ou sobrecarga.
- _Iterator_ permite percorrer uma coleção de elementos (como uma fila de requisições) sem expor sua estrutura interna. Portanto, facilita a navegação sequencial sobre os itens de uma coleção, como uma fila, lista ou conjunto.
