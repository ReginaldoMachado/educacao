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
pytest com cobertura mínima de 50% e o build estrito do MkDocs. Execuções
anteriores para a mesma branch ou pull request são canceladas quando uma nova
execução começa.

## Dependências e segurança

Use Poetry para adicionar, atualizar ou remover dependências e versione as
alterações correspondentes em `pyproject.toml` e `poetry.lock`. Não versione
segredos; configurações sensíveis devem ser fornecidas por mecanismos seguros e
nunca registradas em logs.