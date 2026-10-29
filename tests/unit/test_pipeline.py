import csv
from decimal import Decimal
from pathlib import Path

import pytest

from educacao.pipeline import (
    DataValidationError,
    IdebRecord,
    calculate_variations,
    main,
    read_records,
    run_pipeline,
)

SOURCE = "https://example.org/ideb"
CSV_HEADER = "ano,abrangencia,etapa,rede,ideb,fonte\n"


def write_input(path: Path, rows: str) -> Path:
    path.write_text(CSV_HEADER + rows, encoding="utf-8")
    return path


def test_pipeline_writes_variation_and_reports_counts(tmp_path: Path) -> None:
    input_path = write_input(
        tmp_path / "input.csv",
        f"2023,Brasil,anos_iniciais,publica,5.7,{SOURCE}\n"
        f"2025,Brasil,anos_iniciais,publica,6.1,{SOURCE}\n",
    )
    output_path = tmp_path / "processed" / "output.csv"

    result = run_pipeline(input_path, output_path)

    with output_path.open(encoding="utf-8", newline="") as output_file:
        rows = list(csv.DictReader(output_file))
    assert result.input_count == 2
    assert result.output_count == 1
    assert rows[0]["variacao_ideb"] == "0.4"
    assert rows[0]["ano_inicial"] == "2023"
    assert rows[0]["ano_final"] == "2025"
    assert rows[0]["fonte_inicial"] == SOURCE
    assert rows[0]["fonte_final"] == SOURCE


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        ("wrong,header\n", "Colunas inválidas"),
        (CSV_HEADER, "não contém registros"),
        (CSV_HEADER + f"2023,Brasil,etapa,rede,11,{SOURCE}\n", "entre 0 e 10"),
        (CSV_HEADER + f"2000,Brasil,etapa,rede,5,{SOURCE}\n", "2005 ou posterior"),
        (CSV_HEADER + "2023,Brasil,etapa,rede,abc,fonte\n", "não é numérico"),
        (CSV_HEADER + f"2023,Brasil,etapa,rede,,{SOURCE}\n", "campos obrigatórios vazios"),
    ],
)
def test_read_records_rejects_invalid_input(tmp_path: Path, contents: str, message: str) -> None:
    input_path = tmp_path / "invalid.csv"
    input_path.write_text(contents, encoding="utf-8")

    with pytest.raises(DataValidationError, match=message):
        read_records(input_path)


def test_read_records_rejects_duplicate_observations(tmp_path: Path) -> None:
    input_path = write_input(
        tmp_path / "duplicate.csv",
        f"2023,Brasil,etapa,rede,5,{SOURCE}\n2023,Brasil,etapa,rede,5,{SOURCE}\n",
    )

    with pytest.raises(DataValidationError, match="duplicado"):
        read_records(input_path)


def test_calculate_variations_requires_two_years() -> None:
    record = IdebRecord(2023, "Brasil", "etapa", "rede", Decimal("5"), SOURCE)

    with pytest.raises(DataValidationError, match="ao menos dois anos"):
        calculate_variations([record])


def test_main_returns_error_for_missing_input(tmp_path: Path) -> None:
    result = main(["--input", str(tmp_path / "missing.csv"), "--output", str(tmp_path / "out.csv")])

    assert result == 1
