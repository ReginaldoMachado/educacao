# Desenvolvimento

## Requisitos

- Python compatível com a versão declarada em `pyproject.toml`.
- Poetry para instalar e gerenciar dependências.

## Instalação

```bash
poetry install --sync
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

## Dependências e segurança

Use Poetry para adicionar, atualizar ou remover dependências e versione as
alterações correspondentes em `pyproject.toml` e `poetry.lock`. Não versione
segredos; configurações sensíveis devem ser fornecidas por mecanismos seguros e
nunca registradas em logs.