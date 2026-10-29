# educacao

MVP de engenharia de dados para processar indicadores da Educação Básica
brasileira. O primeiro fluxo calcula a variação do Ideb nacional usando
resultados publicados pelo Inep.

## Status

O pipeline lê o CSV em `data/ideb_brasil.csv`, valida os registros, calcula a
variação entre o primeiro e o último ano de cada série e grava
`data/processed/ideb_variacao.csv`. A amostra de entrada contém resultados
nacionais de 2023 e 2025 transcritos de uma publicação oficial do Inep; não é
uma integração automática com a API do QEdu nem uma base municipal completa.

## Desenvolvimento

O projeto usa Poetry para dependências e ambiente. Execute o pipeline da raiz
do repositório:

```bash
poetry sync
poetry run python -m educacao
```

Para abrir o dashboard interativo no navegador:

```bash
poetry run python -m educacao.dashboard
```

O dashboard abre em `http://127.0.0.1:8000` e permanece ativo até pressionar
`Ctrl+C`. Ele apresenta médias do Ideb, comparação por etapa, variação e filtro
por rede de ensino.

Para processar outro arquivo, use `--input caminho/entrada.csv` e
`--output caminho/saida.csv`. O schema esperado e as limitações da fonte estão
documentados em [Fontes de dados](docs/data-sources.md); comandos de
desenvolvimento e validação estão em [Desenvolvimento](docs/development.md).
