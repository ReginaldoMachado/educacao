# Arquitetura do MVP

## Direção

O primeiro fluxo implementado usa um CSV versionado como entrada e um CSV
local como destino:

1. `python -m educacao` recebe caminhos de entrada e saída;
2. o leitor valida colunas, campos obrigatórios, anos, faixa do Ideb e
   duplicidade;
3. a transformação calcula a diferença entre o primeiro e o último ano por
   abrangência, etapa e rede;
4. o escritor cria o diretório de destino e grava o resultado em CSV.
5. `python -m educacao.dashboard` disponibiliza a mesma entrada validada em
   uma página local com indicadores-resumo, gráfico e filtro por rede.

O código de produção fica em `src/educacao/`. A implementação usa a biblioteca
padrão do Python, sem dependências de runtime adicionais.

## Confiabilidade e observabilidade

O pipeline deve ser reexecutável e idempotente sempre que possível. Integrações
externas terão timeouts e retries definidos somente quando uma integração
externa for implementada. O fluxo atual usa `logging` para registrar início,
fim e contagens, sem incluir dados sensíveis.

## Estado

Este é um pipeline local demonstrativo com resultados agregados publicados pelo
Inep. A ingestão automatizada de uma base oficial completa permanece fora do
escopo até que seu formato e mecanismo de distribuição sejam validados.