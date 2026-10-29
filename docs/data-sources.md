# Fontes de dados

## QEdu

A página institucional do [QEdu](https://portaliede.org.br/qedu/) apresenta
indicadores para Brasil, estados, municípios e escolas, incluindo Ideb,
aprendizado adequado em Língua Portuguesa e Matemática segundo o Saeb, taxas de
aprovação/reprovação/abandono e distorção idade-série.

O material consultado em `doc_api.md` não especifica endpoints, métodos HTTP,
autenticação, parâmetros, formato de resposta ou limites de uso. Portanto, não
há base para implementar uma integração direta com uma API do QEdu.

## Referência metodológica oficial

O [Inep: Índice de Desenvolvimento da Educação Básica
(Ideb)](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/indice-de-desenvolvimento-da-educacao-basica)
informa que o Ideb combina dados de aprovação do Censo Escolar com médias de
desempenho do Saeb. Essa referência ajuda a orientar a descoberta, mas não
valida por si só um dataset, schema ou mecanismo de download.

## Pendências para selecionar a fonte do MVP

- Identificar uma fonte oficial de dados tecnicamente acessível e seus termos
  de uso.
- Confirmar formato, campos, granularidade geográfica e temporal e histórico
  disponível.
- Selecionar um indicador e documentar suas regras e limitações.
- Definir o destino e a frequência de atualização somente depois de validar a
  fonte.

Até essas informações serem confirmadas, nenhuma URL de API, schema ou dado de
exemplo é tratado como contrato real.