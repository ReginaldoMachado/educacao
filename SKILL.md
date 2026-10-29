# SKILL.md — Padrões de Engenharia Python para Engenharia de Dados

## 1. Objetivo

Este documento define o padrão obrigatório de desenvolvimento para projetos Python de Engenharia de Dados neste repositório. Ele serve como referência técnica para engenheiros, revisores e agentes de IA, garantindo consistência, rastreabilidade e qualidade operacional.

A aplicação prática destas regras deve priorizar clareza, simplicidade, manutenção e confiabilidade. O objetivo não é impor burocracia, e sim padronizar práticas que reduzem falhas e aumentam a capacidade de evoluir o sistema com segurança.

## 2. Princípios obrigatórios

### 2.1. Gerenciamento de dependências com Poetry

**Obrigatório:**
- Usar Poetry como única ferramenta para criação, instalação, atualização, remoção e gerenciamento de dependências.
- Nunca utilizar `pip install`, `pip uninstall`, `pip freeze` ou qualquer fluxo manual de criação de ambiente virtual fora do Poetry.
- Executar comandos no ambiente do projeto com `poetry run`.
- Versionar `pyproject.toml` e `poetry.lock`.
- Manter o ambiente virtual gerenciado pelo Poetry e não criar `venv` manualmente salvo exceção explicitamente aprovada.

**Recomendado:**
- Usar grupos de dependências para separar produção e desenvolvimento (`main`, `dev`).
- Revisar alterações em `pyproject.toml` e `poetry.lock` em cada mudança de dependências.
- Atualizar dependências de forma controlada e com testes antes e depois da mudança.

**Exceção:**
- Em cenários excepcionais, a criação de ambiente fora do Poetry pode ser aprovada por consenso do time, mas deve ser documentada e não substitui os padrões do projeto.

### 2.2. Estrutura de projeto em src/

**Obrigatório:**
- Usar a estrutura `src/<nome_do_projeto>/` para código de produção.
- Evitar código de negócio na raiz do projeto.
- Separar produção, testes, documentação, scripts e configurações.
- Garantir que o pacote seja importável de forma consistente após instalação.

**Estrutura recomendada:**

```text
projeto/
├── pyproject.toml
├── poetry.lock
├── README.md
├── .gitignore
├── .env.example
├── mkdocs.yml
├── src/
│   └── projeto/
│       ├── __init__.py
│       ├── config/
│       ├── domain/
│       ├── services/
│       ├── connectors/
│       ├── transformations/
│       ├── pipelines/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
│   ├── index.md
│   ├── architecture.md
│   ├── development.md
│   └── api.md
├── scripts/
└── .github/
```

**Recomendado:**
- Adaptar a estrutura ao tamanho real do projeto.
- Não criar diretórios vazios nem camadas artificiais.
- A organização deve refletir responsabilidades reais do domínio e do pipeline.

### 2.3. Código modular, coeso e desacoplado

**Obrigatório:**
- Cada módulo deve ter responsabilidade clara.
- Separar leitura de dados, validação, transformação e escrita.
- Preferir funções pequenas, bem nomeadas e testáveis.
- Usar type hints em interfaces, funções públicas e pontos de troca de dados.
- Evitar dependências circulares e módulos excessivamente grandes.
- Evitar estado global mutável sem necessidade.
- Evitar abstrações prematuras e duplicação desnecessária.

**Recomendado:**
- Aplicar princípios SOLID quando fizer sentido.
- Usar dataclasses, enums e protocolos quando melhorarem legibilidade e robustez.
- Manter regras de negócio separadas da infraestrutura e das integrações externas.

## 3. Gestão de dependências com Poetry

### 3.1. Fluxo padrão

```bash
poetry new --src projeto
poetry install
poetry add pandas
poetry add --group dev pytest ruff pytest-cov mkdocs-material
poetry remove pandas
poetry update pandas
poetry env info
poetry run python -c "import sys; print(sys.executable)"
poetry run python -m pytest
poetry run ruff check .
poetry run ruff format .
poetry run mkdocs build --strict
```

**Obrigatório:**
- O ambiente do projeto deve ser iniciado e usado via Poetry.
- O Python suportado deve ser explicitado no `pyproject.toml`.
- Dependências de produção e desenvolvimento devem estar bem separadas por grupos.
- A atualização de dependências deve ser feita com atenção ao `poetry.lock` e à compatibilidade da aplicação.

### 3.2. Versão do Python

No `pyproject.toml`, a versão mínima de Python deve refletir o que o projeto realmente suporta. Exemplo:

```toml
[tool.poetry]
name = "educacao"
version = "0.1.0"
description = "Projeto de dados educacionais"
authors = ["Reginaldo Machado <regimachado79@gmail.com>"]

[tool.poetry.dependencies]
python = ">=3.12,<4.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.0"
ruff = "^0.7.0"
pytest-cov = "^5.0.0"
mkdocs-material = "^9.5.0"
```

**Recomendado:**
- Não aumentar a versão mínima de Python sem necessidade.
- Manter a compatibilidade declarada em linha com o ambiente de execução da CI e do time.

## 4. Qualidade de código com Ruff

### 4.1. Padrão obrigatório

**Obrigatório:**
- Ruff como única ferramenta para lint, formatação e organização de imports.
- Configuração centralizada em `pyproject.toml`.
- Execução local antes de commits e integração contínua.
- Correção automática apenas quando segura e revisada.
- Verificação final sem alterações pendentes de lint ou formatação.

**Comandos padrão:**

```bash
poetry add --group dev ruff
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format .
poetry run ruff format --check .
```

### 4.2. Configuração de referência do Ruff

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "B",    # bugbear
    "UP",   # pyupgrade
    "C4",   # comprehensions
    "SIM",  # simplifications
    "N",    # pep8-naming
]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["educacao"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]
```

**Observação:**
- `ruff check --fix` pode corrigir automaticamente problemas suportados, mas o desenvolvedor deve revisar as mudanças.
- Não é aceitável ignorar erros de lint sem justificativa técnica.
- Não se deve introduzir Black, isort ou Flake8 como ferramentas paralelas neste padrão.

## 5. Testes automatizados com pytest

### 5.1. Regras obrigatórias

**Obrigatório:**
- Usar pytest como framework padrão.
- Cobertura mínima global de 50% do código de produção.
- Separar testes unitários e de integração.
- Testes determinísticos, independentes e reproduzíveis.
- Uso de fixtures e parametrização quando apropriado.
- Uso de mocks para isolar dependências externas.
- Casos de sucesso, erro, entradas inválidas e cenários extremos.
- Nomenclatura consistente para arquivos, funções e classes de teste.
- Não reduzir a cobertura para “fazer o pipeline passar”.

**Proibido:**
- Dependência de APIs reais, serviços externos ou bancos de produção em testes unitários.
- Testes fracos que validam apenas o “feliz caminho”.
- Bloquear CI por cobertura artificialmente baixa sem correção do código.

### 5.2. Cobertura mínima

```bash
poetry add --group dev pytest pytest-cov
poetry run pytest tests/unit \
  --cov=educacao \
  --cov-report=term-missing \
  --cov-fail-under=50
```

Exemplo de configuração no `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.coverage.run]
source = ["src/educacao"]
branch = true

[tool.coverage.report]
show_missing = true
skip_covered = true
fail_under = 50
```

**Recomendado:**
- Cobertura superior a 50% em módulos críticos.
- Priorizar regras de negócio, transformações, validações e cálculos.
- Entender que cobertura de linhas não substitui qualidade de testes.

## 6. Documentação com MkDocs Material

**Obrigatório:**
- Usar MkDocs com tema Material como padrão oficial.
- Versionar documentação junto ao código.
- Manter `mkdocs.yml` na raiz do projeto.
- Escrever conteúdo em Markdown em `docs/`.
- Atualizar documentação quando houver mudança relevante em comportamento, arquitetura, operação ou configuração.

**Conteúdo mínimo recomendado:**
- Página inicial com objetivos e escopo.
- Instruções de instalação e desenvolvimento.
- Arquitetura dos módulos principais.
- Configurações obrigatórias.
- Documentação de pipelines e fontes de dados.
- Contratos, schemas e regras de qualidade.
- Exemplos de execução.
- Registro de decisões relevantes.

**Comandos padrão:**

```bash
poetry add --group dev mkdocs-material
poetry run mkdocs serve
poetry run mkdocs build --strict
```

### 6.1. Exemplo mínimo de mkdocs.yml

```yaml
site_name: educacao
site_description: Documentação do projeto de educação
repo_url: https://github.com/seu-usuario/educacao

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - content.code.copy

nav:
  - Início: index.md
  - Desenvolvimento: development.md
  - Arquitetura: architecture.md
  - API: api.md
```

**Obrigatório:**
- O build estrito da documentação deve ser parte da CI.
- Links quebrados, páginas inexistentes e erros de documentação devem falhar o pipeline.

## 7. Boas práticas específicas de Engenharia de Dados

### 7.1. Transformações de dados

**Obrigatório:**
- Separar leitura, validação, transformação e escrita.
- Preferir transformações determinísticas.
- Validar schemas, tipos e campos obrigatórios.
- Definir comportamento explícito para nulos, duplicados, inválidos e atrasados.
- Evitar carregar datasets inteiros em memória sem necessidade.
- Considerar processamento incremental ou por lotes quando apropriado.

**Recomendado:**
- Manter lógica de negócio separada da infraestrutura.
- Evitar acoplamento excessivo entre pipeline e provedor de dados.

### 7.2. Confiabilidade dos pipelines

**Obrigatório:**
- Projetar operações para permitir reexecução segura.
- Priorizar idempotência sempre que possível.
- Tratar falhas e exceções explicitamente.
- Definir retry e timeout para integrações externas.
- Separar parâmetros de execução de regras de negócio.
- Garantir rastreabilidade das execuções.

**Proibido:**
- Captura genérica de exceções sem tratamento ou log útil.
- Repetição de operações não idempotentes sem avaliação dos efeitos colaterais.

### 7.3. Observabilidade

**Obrigatório:**
- Usar o módulo `logging` da biblioteca padrão ou solução padronizada pelo time.
- Registrar início, fim, duração e resultado de etapas relevantes.
- Registrar contagens de entrada, saída, rejeições e métricas relevantes.
- Usar erros úteis para diagnósticos.
- Evitar logs excessivos e dados sensíveis.

**Proibido:**
- Usar `print()` como mecanismo principal de logging em produção.

### 7.4. Configuração e segurança

**Obrigatório:**
- Não armazenar segredos no código, no Git ou na documentação.
- Usar variáveis de ambiente ou mecanismos seguros de gestão de segredos.
- Versionar somente arquivos de exemplo sem credenciais reais.
- Validar configurações no início da execução.
- Não registrar tokens, senhas, dados pessoais sensíveis ou credenciais em logs.
- Não usar SQL gerado por concatenação insegura de strings.
- Não desabilitar validações de segurança para contornar falhas.

### 7.5. Dados e desempenho

**Obrigatório:**
- Escolher estruturas de dados e bibliotecas adequadas ao volume e ao domínio.
- Avaliar uso de memória, CPU, I/O e custo computacional.
- Medir o desempenho antes de introduzir complexidade.
- Definir critérios claros de qualidade dos dados.

**Recomendado:**
- Priorizar qualidade e suporte operacional em vez de otimizações prematuras.

## 8. Tipagem, estilo e legibilidade

**Obrigatório:**
- Usar type hints em funções públicas e interfaces importantes.
- Retornos explícitos nas funções.
- Nomes descritivos para variáveis, funções, classes e módulos.
- Usar `snake_case` para funções e variáveis; `PascalCase` para classes; letras maiúsculas para constantes.
- Tratar erros explicitamente.
- Usar docstrings quando agregarem valor, especialmente em APIs públicas.
- Manter compatibilidade com a versão Python declarada pelo projeto.

**Recomendado:**
- Usar dataclasses, protocolos e tipos específicos quando a semântica do problema justificar.
- Preferir código simples e legível à complexidade artificial.

**Proibido:**
- `Any` indiscriminado sem justificativa.
- Comentários redundantes que repetem o código.
- Funções extremamente longas sem decomposição.

## 9. Git, commits e revisão de código

### 9.1. Regras de colaboração

**Obrigatório:**
- Commits pequenos, objetivos e descritivos.
- Branches com nomes claros e específicos.
- Pull Requests com contexto, motivação e impacto das alterações.
- Revisão de código antes do merge.
- Não versionar `.venv`, `.env` reais, caches, artefatos gerados ou credenciais.
- Revisar alterações em `pyproject.toml` e `poetry.lock`.
- Não misturar alterações sem relação na mesma entrega.

**Recomendado:**
- Respeitar as políticas de proteção da branch principal do repositório.

### 9.2. Checklist mínima de Pull Request

- [ ] A mudança resolve um problema específico ou adiciona funcionalidade clara.
- [ ] O código segue os padrões do projeto.
- [ ] Testes relevantes foram adicionados ou atualizados.
- [ ] Cobertura e lint foram verificados.
- [ ] Documentação foi atualizada quando necessário.
- [ ] Não há segredos, arquivos locais ou artefatos gerados.
- [ ] A mudança é pequena, objetiva e revisável.

## 10. Integração contínua e critérios de qualidade

### 10.1. Verificações mínimas da CI

A CI deve executar, no mínimo:

1. Instalação reproduzível das dependências com Poetry.
2. Verificação de lint com Ruff.
3. Verificação de formatação com Ruff.
4. Testes unitários com pytest.
5. Cobertura mínima de 50%.
6. Build estrito da documentação com MkDocs.

**Comandos recomendados:**

```bash
poetry install --sync
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest tests/unit \
  --cov=educacao \
  --cov-report=term-missing \
  --cov-fail-under=50
poetry run mkdocs build --strict
```

**Observações:**
- Em algumas versões do Poetry, `poetry install --sync` pode não estar disponível. Nesse caso, usar uma alternativa compatível documentada, com a mesma finalidade de ambiente reproduzível.
- A CI deve falhar quando qualquer verificação obrigatória falhar.
- A versão de Python usada na CI deve ser compatível com a declarada no projeto.

## 11. Configuração de referência

### 11.1. Exemplo de `pyproject.toml`

```toml
[tool.poetry]
name = "educacao"
version = "0.1.0"
description = "Projeto de dados educacionais"
authors = ["Reginaldo Machado <regimachado79@gmail.com>"]
packages = [{ include = "educacao", from = "src" }]

[tool.poetry.dependencies]
python = ">=3.12,<4.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.0"
pytest-cov = "^5.0.0"
ruff = "^0.7.0"
mkdocs-material = "^9.5.0"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",
    "F",
    "I",
    "B",
    "UP",
    "C4",
    "SIM",
    "N",
]

[tool.ruff.lint.isort]
known-first-party = ["educacao"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

[tool.coverage.run]
source = ["src/educacao"]
branch = true

[tool.coverage.report]
show_missing = true
skip_covered = true
fail_under = 50

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

### 11.2. Exemplo de módulo de transformação

```python
from __future__ import annotations

from typing import Iterable


def normalize_school_name(name: str) -> str:
    return " ".join(name.strip().split()).title()


def filter_valid_records(records: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    valid_records: list[dict[str, object]] = []

    for record in records:
        if not record.get("school_name"):
            continue
        normalized = dict(record)
        normalized["school_name"] = normalize_school_name(str(record["school_name"]))
        valid_records.append(normalized)

    return valid_records
```

### 11.3. Exemplo de teste unitário

```python
from educacao.transformations import filter_valid_records


def test_filter_valid_records_keeps_only_valid_rows() -> None:
    rows = [
        {"school_name": " escola alfa ", "value": 10},
        {"school_name": "", "value": 11},
        {"school_name": "escola beta", "value": 12},
    ]

    result = filter_valid_records(rows)

    assert result[0]["school_name"] == "Escola Alfa"
    assert len(result) == 2
```

## 12. Como este SKILL.md orienta agentes de IA

Qualquer agente de IA deve:

1. Ler a estrutura existente antes de alterar arquivos.
2. Identificar a versão de Python e do Poetry utilizadas pelo projeto.
3. Respeitar os padrões estabelecidos, salvo motivo técnico explícito.
4. Preferir mudanças pequenas, localizadas e revisáveis.
5. Reusar componentes existentes antes de criar duplicações.
6. Não introduzir dependências sem necessidade estrita.
7. Nunca usar `pip` para instalar, remover ou atualizar pacotes.
8. Não reduzir cobertura nem desabilitar regras para esconder falhas.
9. Não afirmar que testes, lint, formatação ou documentação passaram sem executá-los.
10. Executar verificações relevantes após as alterações.
11. Informar claramente verificações executadas, resultados, limitações e pendências.
12. Não expor dados sensíveis ou credenciais.
13. Não reescrever arquivos de configuração inteiros quando uma alteração pontual basta.

Quando não for possível executar algum comando, o agente deve informar a limitação sem declarações de sucesso.

## 13. Checklist de conclusão de tarefa

Antes de encerrar uma tarefa, verificar:

- [ ] Estrutura e responsabilidades do projeto foram respeitadas.
- [ ] Dependências foram geridas via Poetry.
- [ ] Lint e formatação foram executados.
- [ ] Testes relevantes passaram.
- [ ] Cobertura mínima foi mantida.
- [ ] Documentação foi atualizada quando necessário.
- [ ] Alterações foram revisadas para não incluir ruído ou arquivos de ambiente.
- [ ] Nenhum segredo ou dado sensível foi exposto.

## 14. Regra final de governança

Este documento não autoriza agentes de IA nem desenvolvedores a ignorar testes, contornar regras do projeto ou inventar resultados. O cumprimento de critérios objetivos de qualidade é obrigatório: validação real, revisão técnica e documentação consistente são parte do processo de entrega.

A padronização aqui descrita deve servir como base para uma engenharia de dados confiável, sustentável e segura, em vez de um conjunto de boas práticas genéricas sem aplicação prática.
