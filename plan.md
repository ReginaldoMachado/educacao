# Plano de criação do projeto Educacao

## Problema e abordagem

Criar um MVP de engenharia de dados para indicadores educacionais, seguindo os padrões definidos em `SKILL.md`. A página institucional do QEdu não especifica contrato de API. Para tornar o projeto executável sem inventar uma integração, o primeiro fluxo usa valores nacionais do Ideb publicados pelo Inep, transcritos para um CSV versionado e processados localmente.

O repositório já tem uma base inicial: pacote em `src/educacao`, testes, documentação, configuração Poetry e dependências de desenvolvimento. As etapas devem evoluir essa estrutura, sem recriá-la nem adicionar camadas sem necessidade.

## Etapas

1. **Descobrir e delimitar a fonte do MVP**
   - Concluído para o fluxo demonstrativo: usar a publicação oficial do [Inep sobre os resultados do Ideb de 2025](https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica), que compara resultados nacionais de 2023 e 2025.
   - Registrar no CSV a abrangência, etapa, rede, ano, valor e origem; documentar que são resultados agregados nacionais, não uma base integral.
   - Manter uma futura integração com base oficial completa como pendência até validar seu mecanismo de distribuição e schema.

2. **Consolidar a base técnica e os contratos**
   - Base Poetry/Python 3.12 mantida sem dependências de runtime adicionais.
   - Contrato CSV implementado em `src/educacao/pipeline.py`; valida campos obrigatórios, tipos, anos, faixa do Ideb e duplicidade.
   - Não há segredos nem configuração externa necessária neste fluxo local.

3. **Implementar o pipeline inicial**
   - Concluído: `poetry run python -m educacao` lê o CSV, valida, calcula a variação entre o primeiro e o último ano por série e grava `data/processed/ideb_variacao.csv`.
   - O fluxo é determinístico e reexecutável, registra contagens com `logging` e encerra com erro explícito para entrada inválida ou inacessível.

4. **Validar qualidade e integração contínua**
   - Testes unitários determinísticos cobrem transformação, schema, registros inválidos, duplicidade e falhas de leitura.
   - Cobertura do código de produção acima do mínimo de 50%; validações executadas pela CI existente.
   - Não há teste de integração com serviço externo porque a fonte atual é um CSV local.
   - Os comandos de validação são executados diretamente com Poetry; Taskipy não é necessário para este MVP.

5. **Documentar e demonstrar o MVP**
   - README e documentação MkDocs descrevem fonte, limitações, schema, arquitetura, execução e erros.
   - Fluxo e comandos validados no ambiente Poetry do projeto.

## Critérios de conclusão

- Existe uma publicação oficial identificada e documentada; a amostra e a limitação de não ser uma base integral são explícitas.
- O pipeline local executa leitura, validação, transformação e gravação com tratamento explícito de falhas e logs úteis.
- Testes cobrem os principais cenários e atingem pelo menos 50% de cobertura.
- Ruff, testes/cobertura e build estrito do MkDocs passam na validação local e na CI.
- Instruções e limitações do MVP estão documentadas, sem credenciais ou dados sensíveis versionados.

## Considerações

- O MVP atual processa uma amostra de resultados nacionais do Ideb de 2023 e 2025; a atualização não é automática.
- O destino atual é CSV local. Base completa, granularidade subnacional e frequência de atualização dependem da validação de uma fonte de dados distribuída pelo Inep.
- `doc_api.md` descreve o QEdu, mas não constitui documentação técnica de API.
- Seguir `SKILL.md`: Poetry como único gerenciador de dependências, código de produção em `src/`, pytest, Ruff, MkDocs Material, tipagem, observabilidade e segurança.
- A configuração atual usa Python `>=3.12`, pacote `educacao` em `src/` e grupos de dependências Poetry; confirmar compatibilidade com CI antes de ajustar versões.
