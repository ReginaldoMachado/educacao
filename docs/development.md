# Desenvolvimento

## Requisitos

- Python compatível com a versão declarada em `pyproject.toml`.
- Poetry para instalar e gerenciar dependências.

## Instalação

```bash
poetry sync
```

Execute os comandos dentro do ambiente gerenciado pelo Poetry:

```bash
poetry run python --version
poetry run pytest
```

## Executar o pipeline

Na raiz do repositório:

```bash
poetry run python -m educacao
```

O comando usa `data/ideb_brasil.csv` como entrada e grava
`data/processed/ideb_variacao.csv`. Para especificar arquivos:

```bash
poetry run python -m educacao --input caminho/entrada.csv --output caminho/saida.csv
```

Uma entrada inválida ou um arquivo inacessível encerra o comando com código
de saída diferente de zero e uma mensagem de erro.

## Abrir o dashboard

Para abrir a página no navegador e servir os dados locais:

```bash
poetry run python -m educacao.dashboard
```

O servidor fica disponível em `http://127.0.0.1:8000` e é encerrado com
`Ctrl+C`. Também aceita `--input caminho/entrada.csv`, `--host` e `--port`.
Para iniciar sem abrir o navegador automaticamente, use `--no-browser`.
O dashboard mostra médias do Ideb e variações por etapa, com filtro por rede.

## Verificações

```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest tests/unit --cov=educacao --cov-report=term-missing --cov-fail-under=50
poetry run mkdocs build --strict
```

Os testes unitários não devem depender de APIs reais ou serviços externos. As
regras de domínio e transformação devem ter testes determinísticos, incluindo
entradas inválidas e casos extremos.

## Integração contínua

O GitHub Actions executa as verificações de qualidade em pushes, pull requests
e também pode ser iniciado manualmente pela aba **Actions**. O workflow valida
o lockfile, instala as dependências sincronizadas com Poetry e executa Ruff,
pytest com cobertura mínima de 50%, o pipeline de demonstração e o build
estrito do MkDocs. Execuções
anteriores para a mesma branch ou pull request são canceladas quando uma nova
execução começa.

## Dependências e segurança

Use Poetry para adicionar, atualizar ou remover dependências e versione as
alterações correspondentes em `pyproject.toml` e `poetry.lock`. Não versione
segredos; configurações sensíveis devem ser fornecidas por mecanismos seguros e
nunca registradas em logs.