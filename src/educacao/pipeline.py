"""Pipeline local para calcular a variação do Ideb a partir de um CSV."""

from __future__ import annotations

import argparse
import csv
import logging
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

LOGGER = logging.getLogger(__name__)
INPUT_COLUMNS = ("ano", "abrangencia", "etapa", "rede", "ideb", "fonte")
OUTPUT_COLUMNS = (
    "abrangencia",
    "etapa",
    "rede",
    "ano_inicial",
    "ideb_inicial",
    "ano_final",
    "ideb_final",
    "variacao_ideb",
    "fonte_inicial",
    "fonte_final",
)


class DataValidationError(ValueError):
    """Indica que a entrada não atende ao contrato do pipeline."""


@dataclass(frozen=True)
class IdebRecord:
    ano: int
    abrangencia: str
    etapa: str
    rede: str
    ideb: Decimal
    fonte: str


@dataclass(frozen=True)
class PipelineResult:
    input_count: int
    output_count: int
    output_path: Path


def read_records(input_path: Path) -> list[IdebRecord]:
    """Lê e valida o schema e as regras básicas do CSV de entrada."""
    try:
        with input_path.open(encoding="utf-8-sig", newline="") as input_file:
            reader = csv.DictReader(input_file)
            if reader.fieldnames != list(INPUT_COLUMNS):
                raise DataValidationError(
                    f"Colunas inválidas em {input_path}; esperadas: {', '.join(INPUT_COLUMNS)}."
                )
            records = [_parse_record(row, line_number) for line_number, row in enumerate(reader, 2)]
    except csv.Error as error:
        raise DataValidationError(f"CSV inválido em {input_path}: {error}") from error

    if not records:
        raise DataValidationError(f"O arquivo {input_path} não contém registros.")

    seen: set[tuple[int, str, str, str]] = set()
    for record in records:
        key = (record.ano, record.abrangencia, record.etapa, record.rede)
        if key in seen:
            raise DataValidationError(
                f"Registro duplicado para ano={record.ano}, "
                f"abrangencia={record.abrangencia}, etapa={record.etapa}, rede={record.rede}."
            )
        seen.add(key)

    return records


def _parse_record(row: dict[str | None, str | None], line_number: int) -> IdebRecord:
    if None in row or any(row.get(column) is None for column in INPUT_COLUMNS):
        raise DataValidationError(f"Linha {line_number}: número de colunas inválido.")

    values = {column: (row[column] or "").strip() for column in INPUT_COLUMNS}
    if any(not value for value in values.values()):
        raise DataValidationError(f"Linha {line_number}: há campos obrigatórios vazios.")

    try:
        year = int(values["ano"])
        score = Decimal(values["ideb"])
    except (ValueError, InvalidOperation) as error:
        raise DataValidationError(
            f"Linha {line_number}: ano ou valor do Ideb não é numérico."
        ) from error

    if year < 2005:
        raise DataValidationError(f"Linha {line_number}: o ano do Ideb deve ser 2005 ou posterior.")
    if not score.is_finite() or not Decimal("0") <= score <= Decimal("10"):
        raise DataValidationError(f"Linha {line_number}: o Ideb deve estar entre 0 e 10.")

    return IdebRecord(
        ano=year,
        abrangencia=values["abrangencia"],
        etapa=values["etapa"],
        rede=values["rede"],
        ideb=score,
        fonte=values["fonte"],
    )


def calculate_variations(records: list[IdebRecord]) -> list[dict[str, str]]:
    """Calcula a diferença entre o primeiro e o último ano de cada série."""
    groups: dict[tuple[str, str, str], list[IdebRecord]] = defaultdict(list)
    for record in records:
        groups[(record.abrangencia, record.etapa, record.rede)].append(record)

    results: list[dict[str, str]] = []
    for (abrangencia, etapa, rede), observations in sorted(groups.items()):
        observations.sort(key=lambda record: record.ano)
        if len(observations) < 2:
            raise DataValidationError(
                f"Série sem comparação para abrangencia={abrangencia}, etapa={etapa}, rede={rede}; "
                "informe ao menos dois anos."
            )

        first, last = observations[0], observations[-1]
        results.append(
            {
                "abrangencia": abrangencia,
                "etapa": etapa,
                "rede": rede,
                "ano_inicial": str(first.ano),
                "ideb_inicial": str(first.ideb),
                "ano_final": str(last.ano),
                "ideb_final": str(last.ideb),
                "variacao_ideb": str(last.ideb - first.ideb),
                "fonte_inicial": first.fonte,
                "fonte_final": last.fonte,
            }
        )

    return results


def write_results(output_path: Path, results: list[dict[str, str]]) -> None:
    """Grava o resultado em CSV, criando o diretório de destino se necessário."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)


def run_pipeline(input_path: Path, output_path: Path) -> PipelineResult:
    """Executa leitura, validação, transformação e gravação do pipeline."""
    LOGGER.info("Iniciando pipeline do Ideb: %s", input_path)
    records = read_records(input_path)
    results = calculate_variations(records)
    write_results(output_path, results)
    LOGGER.info(
        "Pipeline concluído: %d registros lidos, %d séries gravadas em %s",
        len(records),
        len(results),
        output_path,
    )
    return PipelineResult(len(records), len(results), output_path)


def main(argv: Sequence[str] | None = None) -> int:
    """Ponto de entrada da CLI."""
    parser = argparse.ArgumentParser(description="Calcula a variação do Ideb a partir de um CSV.")
    parser.add_argument("--input", type=Path, default=Path("data/ideb_brasil.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/ideb_variacao.csv"))
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        run_pipeline(args.input, args.output)
    except (DataValidationError, OSError) as error:
        LOGGER.error("Pipeline não concluído: %s", error)
        return 1
    return 0
