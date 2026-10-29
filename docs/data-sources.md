# Fontes de dados

## QEdu

A página institucional do [QEdu](https://portaliede.org.br/qedu/) apresenta
indicadores para Brasil, estados, municípios e escolas, incluindo Ideb,
aprendizado adequado em Língua Portuguesa e Matemática segundo o Saeb, taxas de
aprovação/reprovação/abandono e distorção idade-série.

O material consultado em `doc_api.md` não especifica endpoints, métodos HTTP,
autenticação, parâmetros, formato de resposta ou limites de uso. Portanto, não
há base para implementar uma integração direta com uma API do QEdu.

## Fonte do primeiro fluxo: Ideb nacional

O [Inep publicou os resultados do Ideb de 2025](https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica),
com comparações nacionais a 2023. O arquivo `data/ideb_brasil.csv` registra
esses valores publicados para Brasil, três etapas de ensino e duas categorias
de rede. Os valores foram transcritos da publicação para demonstrar um fluxo
reprodutível; o arquivo não é um download integral da base do Inep.

O Inep explica que o Ideb combina aprovação escolar do Censo Escolar com
desempenho no Saeb. A página institucional do [QEdu](https://portaliede.org.br/qedu/)
é uma referência de domínio, mas não publica contrato técnico de API. Por isso,
este MVP não presume endpoints, autenticação ou formato de integração com o QEdu.

### Contrato do CSV de entrada

| Coluna | Regra |
| --- | --- |
| `ano` | Ano inteiro, 2005 ou posterior |
| `abrangencia` | Recorte geográfico não vazio |
| `etapa` | Etapa de ensino não vazia |
| `rede` | Categoria de rede não vazia |
| `ideb` | Número entre 0 e 10 |
| `fonte` | URL ou identificação da origem, não vazia |

Cada combinação de ano, abrangência, etapa e rede deve ser única. Cada série
comparada precisa ter pelo menos dois anos. O pipeline calcula a diferença
entre o primeiro e o último ano disponível, em pontos de Ideb, sem inferir
anos ausentes.

O resultado `data/processed/ideb_variacao.csv` contém abrangência, etapa, rede,
anos inicial e final, valores do Ideb, variação em pontos e a fonte de cada
observação comparada.

## Limitações e próximos passos

- A amostra contém apenas resultados agregados nacionais de 2023 e 2025; não
  substitui uma base completa de escolas, municípios ou estados.
- A entrada é estática e sua atualização exige validar e incorporar novos
  dados publicados pelo Inep; não há atualização automática nem frequência
  programada.
- O destino atual é um CSV local em `data/processed/`.
- Uma integração automática dependerá de localizar e validar um mecanismo
  oficial de distribuição e seu schema.