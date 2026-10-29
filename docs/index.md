# Educacao

Este projeto organiza um MVP executável de engenharia de dados para indicadores
da Educação Básica brasileira. O primeiro pipeline valida observações nacionais
do Ideb publicadas pelo Inep e calcula sua variação entre anos.

## Estado atual

O fluxo local é executado com `poetry run python -m educacao`. Ele usa um CSV
demonstrativo baseado em resultados agregados publicados pelo Inep; não há
integração automática com a API do QEdu.

## Navegação

- [Arquitetura](architecture.md): responsabilidades previstas para o MVP.
- [Fontes de dados](data-sources.md): referências consultadas e pendências.
- [Desenvolvimento](development.md): ambiente e verificações locais.