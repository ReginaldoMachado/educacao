import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from educacao.dashboard import build_dashboard_data, create_handler, render_dashboard


def test_dashboard_data_uses_validated_pipeline_records() -> None:
    data = build_dashboard_data(Path("data/ideb_brasil.csv"))

    assert data["source_count"] == 12
    assert len(data["records"]) == 6
    assert data["records"][0]["variacao_ideb"] == "0.3"


def test_render_dashboard_escapes_data_inside_json_script() -> None:
    html = render_dashboard(
        {
            "source_count": 1,
            "records": [
                {
                    "abrangencia": "</script><script>alert(1)</script>",
                    "etapa": "anos_iniciais",
                    "rede": "publica",
                    "ano_inicial": "2023",
                    "ideb_inicial": "5.0",
                    "ano_final": "2025",
                    "ideb_final": "6.0",
                    "variacao_ideb": "1.0",
                    "fonte_inicial": "https://example.org",
                    "fonte_final": "https://example.org",
                }
            ],
        }
    )

    assert "</script><script>alert(1)</script>" not in html
    serialized_data = html.split('<script id="dashboard-data" type="application/json">')[1].split(
        "</script>", maxsplit=1
    )[0]
    assert json.loads(serialized_data)["records"][0]["abrangencia"].startswith("</script>")


def test_dashboard_http_endpoint_returns_page_and_data() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(Path("data/ideb_brasil.csv")))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        connection.request("GET", "/")
        response = connection.getresponse()
        body = response.read().decode("utf-8")
        connection.close()
        assert response.status == 200
        assert "Painel do Ideb" in body
        assert "Gráfico de barras comparando Ideb por etapa" in body
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_dashboard_returns_404_for_unknown_path() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(Path("data/ideb_brasil.csv")))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        connection.request("GET", "/unknown")
        response = connection.getresponse()
        response.read()
        connection.close()
        assert response.status == 404
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
