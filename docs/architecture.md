# Arquitetura do MVP

## Direção

A arquitetura deve refletir apenas as responsabilidades necessárias ao
primeiro fluxo, mantendo regras de domínio separadas do acesso à fonte:

1. configuração e validação dos parâmetros de execução;
2. leitura da fonte confirmada;
3. validação do schema e das regras de qualidade;
4. transformação determinística do indicador escolhido;
5. gravação em um destino definido após a descoberta da fonte.

O código de produção ficará em `src/educacao/`. Os módulos serão criados
conforme as responsabilidades reais do pipeline, evitando diretórios e
abstrações prematuros.

## Confiabilidade e observabilidade

O pipeline deve ser reexecutável e idempotente sempre que possível. Integrações
externas terão timeouts e retries definidos de acordo com o mecanismo
confirmado. Etapas relevantes usarão `logging` para registrar início, fim,
resultado e contagens, sem incluir credenciais ou dados sensíveis.

## Estado

Esta é a arquitetura-alvo do MVP. A fonte e o destino ainda não foram
selecionados porque as referências atuais não definem um contrato de
integração.