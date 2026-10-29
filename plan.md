# Plano de criação do projeto Educacao

## Problema e abordagem

Criar um MVP de engenharia de dados para trabalhar com indicadores educacionais do QEdu, seguindo os padrões definidos em `SKILL.md`. Como `doc_api.md` é uma referência institucional e não especifica endpoints, autenticação ou formatos de resposta, a primeira etapa será validar fontes oficiais e tecnicamente acessíveis. O plano não presume endpoints nem acesso a uma API privada; a implementação do pipeline dependerá dessa descoberta.

O repositório já tem uma base inicial: pacote em `src/educacao`, testes, documentação, configuração Poetry e dependências de desenvolvimento. As etapas devem evoluir essa estrutura, sem recriá-la nem adicionar camadas sem necessidade.

## Etapas

1. **Descobrir e delimitar a fonte do MVP**
   - Investigar fontes oficiais e utilizáveis para os indicadores citados em `doc_api.md` (Ideb, Saeb/aprendizado adequado, fluxo escolar e distorção idade-série).
   - Confirmar formato de acesso, disponibilidade, termos de uso, campos, granularidade geográfica e temporal.
   - Escolher uma fonte e um indicador para o primeiro fluxo; registrar limitações e critérios de atualização.
   - Se não houver API documentada e acessível, priorizar uma fonte pública validada em arquivo ou outro mecanismo oficial, sem inventar contratos.

2. **Consolidar a base técnica e os contratos**
   - Conferir a configuração existente de Poetry, versão Python suportada e dependências; manter `pyproject.toml` e `poetry.lock` consistentes.
   - Organizar somente os módulos necessários em `src/educacao`, separando configuração, acesso à fonte, validação, transformações e pipeline conforme responsabilidades reais.
   - Definir o schema e as regras de qualidade do indicador escolhido, incluindo nulos, duplicados, tipos e registros inválidos.
   - Usar configuração validada por variáveis de ambiente quando necessário; não versionar nem registrar segredos.

3. **Implementar o pipeline inicial**
   - Implementar leitura da fonte confirmada, validação do contrato, transformação determinística e gravação no destino acordado após a descoberta.
   - Tornar a execução reexecutável e idempotente quando possível; configurar timeout e retry apenas conforme o mecanismo de acesso exigir.
   - Registrar início, fim, resultado, contagens de entrada/saída e rejeições usando `logging`, sem expor dados sensíveis.
   - Tratar falhas explicitamente e produzir erros úteis para diagnóstico.

4. **Validar qualidade e integração contínua**
   - Criar testes unitários determinísticos para regras, transformações, entradas inválidas e casos extremos; isolar sistemas externos com mocks.
   - Adicionar testes de integração apropriados à fonte escolhida, sem depender de serviços reais nos testes unitários.
   - Atender à cobertura global mínima de 50% do código de produção.
   - Planejar atalhos de validação com Taskipy: `poetry run task lint` para o Ruff, `poetry run task format` para formatar o código e `poetry run task docs` para gerar a documentação com MkDocs.
   - Configurar CI para instalar dependências via Poetry e executar Ruff (lint e formatação), pytest com cobertura e `mkdocs build --strict`.

5. **Documentar e demonstrar o MVP**
   - Atualizar `README.md` e a documentação MkDocs com escopo, fonte e limitações, arquitetura, instalação, configuração e instruções de execução.
   - Documentar schema, regras de qualidade, exemplo de execução e comportamento diante de falhas.
   - Validar o fluxo e os comandos documentados em um ambiente reproduzível gerenciado pelo Poetry.

## Critérios de conclusão

- Existe uma fonte oficial validada e documentada, sem endpoints ou contratos presumidos.
- O pipeline inicial executa leitura, validação, transformação e gravação com tratamento explícito de falhas e logs úteis.
- Testes cobrem os principais cenários e atingem pelo menos 50% de cobertura.
- Ruff, testes/cobertura e build estrito do MkDocs passam na validação local e na CI.
- Instruções e limitações do MVP estão documentadas, sem credenciais ou dados sensíveis versionados.

## Considerações

- O escopo aprovado é um MVP, começando pela descoberta da fonte; o indicador, o destino e a frequência de atualização permanecem decisões posteriores à validação dos dados disponíveis.
- `doc_api.md` descreve o QEdu, mas não constitui documentação técnica de API.
- Seguir `SKILL.md`: Poetry como único gerenciador de dependências, código de produção em `src/`, pytest, Ruff, MkDocs Material, tipagem, observabilidade e segurança.
- A configuração atual usa Python `>=3.12`, pacote `educacao` em `src/` e grupos de dependências Poetry; confirmar compatibilidade com CI antes de ajustar versões.
