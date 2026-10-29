"""Dashboard web local para os resultados agregados do Ideb."""

# The inline HTML template contains long CSS and JavaScript lines.
# ruff: noqa: E501
from __future__ import annotations

import argparse
import html
import json
import logging
import webbrowser
from collections.abc import Sequence
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from educacao.pipeline import calculate_variations, read_records

LOGGER = logging.getLogger(__name__)


def build_dashboard_data(input_path: Path) -> dict[str, Any]:
    records = read_records(input_path)
    return {
        "records": calculate_variations(records),
        "source_count": len(records),
    }


def render_dashboard(data: dict[str, Any]) -> str:
    serialized_data = json.dumps(data, ensure_ascii=False)
    serialized_data = (
        serialized_data.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    )
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f5f7f4">
  <title>Educacao | Painel do Ideb</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
      color: #17231e;
      background: #f5f7f4;
      font-synthesis: none;
      text-rendering: optimizeLegibility;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-width: 320px; }}
    .shell {{ max-width: 1160px; margin: 0 auto; padding: 38px 28px 44px; }}
    header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; }}
    .eyebrow {{ color: #557267; font-size: 12px; font-weight: 750; letter-spacing: .13em; text-transform: uppercase; }}
    h1 {{ margin: 10px 0 8px; font-size: clamp(30px, 5vw, 46px); letter-spacing: -.045em; }}
    .subtitle {{ color: #65756e; margin: 0; line-height: 1.6; }}
    .badge {{ border: 1px solid #dce5df; border-radius: 999px; padding: 9px 13px; white-space: nowrap; color: #3b6654; font-size: 12px; font-weight: 700; }}
    .toolbar {{ display: flex; align-items: center; gap: 10px; margin: 30px 0 16px; }}
    label {{ color: #617168; font-size: 13px; font-weight: 650; }}
    select {{ padding: 10px 36px 10px 12px; border: 1px solid #d7e0da; border-radius: 9px; background: white; color: #17231e; font: inherit; }}
    .cards {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
    .card, .panel {{ background: white; border: 1px solid #e6ebe7; border-radius: 14px; box-shadow: 0 5px 18px #213c2a08; }}
    .card {{ padding: 19px 20px; }}
    .card-label {{ color: #718078; font-size: 13px; }}
    .card-value {{ display: block; margin-top: 12px; font-size: 32px; font-weight: 760; letter-spacing: -.04em; }}
    .card-note {{ color: #829087; display: block; margin-top: 5px; font-size: 12px; }}
    .content {{ display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(300px, .9fr); gap: 14px; margin-top: 14px; }}
    .panel {{ padding: 22px; min-width: 0; }}
    .panel-heading {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }}
    h2 {{ margin: 0; font-size: 17px; letter-spacing: -.02em; }}
    .panel-note {{ color: #7a8981; font-size: 12px; margin: 6px 0 0; }}
    .legend {{ display: flex; gap: 13px; color: #6d7a73; font-size: 11px; }}
    .legend span {{ display: flex; align-items: center; gap: 5px; }}
    .dot {{ width: 8px; height: 8px; display: inline-block; border-radius: 50%; background: #cbd9d0; }}
    .dot.current {{ background: #277451; }}
    #chart {{ display: grid; gap: 20px; padding-top: 30px; }}
    .bar-row {{ display: grid; grid-template-columns: 110px minmax(0, 1fr); align-items: center; gap: 12px; }}
    .bar-label {{ color: #53645b; font-size: 12px; }}
    .bar-pair {{ display: grid; gap: 5px; }}
    .bar-line {{ display: flex; align-items: center; gap: 8px; height: 13px; }}
    .bar {{ height: 9px; min-width: 3px; border-radius: 99px; background: #cbd9d0; transition: width .25s ease; }}
    .bar.current {{ background: #277451; }}
    .bar-value {{ color: #5f7067; font-size: 11px; font-variant-numeric: tabular-nums; }}
    .table-wrap {{ overflow-x: auto; margin-top: 20px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    th {{ color: #829087; font-size: 10px; font-weight: 700; letter-spacing: .07em; text-align: left; text-transform: uppercase; }}
    th, td {{ padding: 11px 8px; border-bottom: 1px solid #edf0ed; white-space: nowrap; }}
    td {{ color: #46564d; font-variant-numeric: tabular-nums; }}
    th:first-child, td:first-child {{ padding-left: 0; }}
    tr:last-child td {{ border-bottom: 0; }}
    .delta {{ color: #277451; font-weight: 750; }}
    .source {{ margin-top: 15px; color: #849087; font-size: 11px; line-height: 1.6; }}
    .source a {{ color: #277451; text-underline-offset: 3px; }}
    footer {{ margin-top: 18px; color: #849087; font-size: 11px; line-height: 1.6; }}
    @media (max-width: 760px) {{
      .shell {{ padding: 26px 16px 34px; }}
      header {{ display: block; }}
      .badge {{ display: inline-block; margin-top: 18px; }}
      .content {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 520px) {{
      .cards {{ grid-template-columns: 1fr; }}
      .card {{ padding: 16px; }}
      .card-value {{ font-size: 27px; }}
      .panel {{ padding: 17px; }}
      .bar-row {{ grid-template-columns: 88px minmax(0, 1fr); gap: 8px; }}
      .legend {{ gap: 7px; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div>
        <div class="eyebrow">Educacao · Indicadores educacionais</div>
        <h1>Painel do Ideb</h1>
        <p class="subtitle">Evolução do Índice de Desenvolvimento da Educação Básica no Brasil.</p>
      </div>
      <div class="badge">Dados agregados · Inep</div>
    </header>

    <div class="toolbar">
      <label for="network">Rede de ensino</label>
      <select id="network" aria-label="Filtrar por rede de ensino"></select>
    </div>

    <section class="cards" aria-label="Indicadores resumo">
      <article class="card">
        <span class="card-label">Ideb médio · ano inicial</span>
        <strong class="card-value" id="start-average">—</strong>
        <span class="card-note" id="start-year">—</span>
      </article>
      <article class="card">
        <span class="card-label">Ideb médio · ano final</span>
        <strong class="card-value" id="end-average">—</strong>
        <span class="card-note" id="end-year">—</span>
      </article>
      <article class="card">
        <span class="card-label">Variação média</span>
        <strong class="card-value" id="average-change">—</strong>
        <span class="card-note">pontos do Ideb nas etapas exibidas</span>
      </article>
    </section>

    <section class="content">
      <article class="panel">
        <div class="panel-heading">
          <div>
            <h2>Ideb por etapa de ensino</h2>
            <p class="panel-note">Comparação dos anos inicial e final disponíveis</p>
          </div>
          <div class="legend" aria-label="Legenda do gráfico">
            <span><i class="dot"></i><span id="legend-start">Inicial</span></span>
            <span><i class="dot current"></i><span id="legend-end">Final</span></span>
          </div>
        </div>
        <div id="chart" role="img" aria-label="Gráfico de barras comparando Ideb por etapa"></div>
        <div class="source" id="source"></div>
      </article>

      <article class="panel">
        <h2>Detalhamento</h2>
        <p class="panel-note">Resultados para cada etapa selecionada</p>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Etapa</th><th>Inicial</th><th>Final</th><th>Variação</th></tr></thead>
            <tbody id="results"></tbody>
          </table>
        </div>
      </article>
    </section>
    <footer id="disclaimer"></footer>
  </main>
  <script id="dashboard-data" type="application/json">{serialized_data}</script>
  <script>
    const data = JSON.parse(document.getElementById("dashboard-data").textContent);
    const names = {{
      anos_iniciais: "Anos iniciais",
      anos_finais: "Anos finais",
      ensino_medio: "Ensino médio"
    }};
    const networks = [...new Set(data.records.map((item) => item.rede))];
    const selector = document.getElementById("network");
    const networkNames = {{ publica: "Rede pública", publicas_e_privadas: "Públicas e privadas" }};

    for (const network of networks) {{
      const option = document.createElement("option");
      option.value = network;
      option.textContent = networkNames[network] || network;
      selector.append(option);
    }}

    function showDashboard() {{
      const rows = data.records
        .filter((item) => item.rede === selector.value)
        .sort((left, right) => left.etapa.localeCompare(right.etapa));
      const average = (field) =>
        rows.reduce((total, item) => total + Number(item[field]), 0) / rows.length;
      const startYear = rows[0].ano_inicial;
      const endYear = rows[0].ano_final;
      const change = average("variacao_ideb");

      document.getElementById("start-average").textContent = average("ideb_inicial").toFixed(1);
      document.getElementById("end-average").textContent = average("ideb_final").toFixed(1);
      document.getElementById("average-change").textContent =
        `${{change >= 0 ? "+" : ""}}${{change.toFixed(1)}}`;
      document.getElementById("start-year").textContent = `Média das etapas em ${{startYear}}`;
      document.getElementById("end-year").textContent = `Média das etapas em ${{endYear}}`;
      document.getElementById("legend-start").textContent = startYear;
      document.getElementById("legend-end").textContent = endYear;

      const chart = document.getElementById("chart");
      chart.replaceChildren();
      const table = document.getElementById("results");
      table.replaceChildren();
      for (const item of rows) {{
        const label = names[item.etapa] || item.etapa;
        const pair = document.createElement("div");
        pair.className = "bar-row";
        const title = document.createElement("span");
        title.className = "bar-label";
        title.textContent = label;
        const bars = document.createElement("div");
        bars.className = "bar-pair";
        for (const [field, isCurrent] of [["ideb_inicial", false], ["ideb_final", true]]) {{
          const line = document.createElement("div");
          line.className = "bar-line";
          const bar = document.createElement("span");
          bar.className = isCurrent ? "bar current" : "bar";
          bar.style.width = `${{Math.max(Number(item[field]) * 10, 2)}}%`;
          const value = document.createElement("span");
          value.className = "bar-value";
          value.textContent = Number(item[field]).toFixed(1);
          line.append(bar, value);
          bars.append(line);
        }}
        pair.append(title, bars);
        chart.append(pair);

        const row = document.createElement("tr");
        for (const [value, className] of [
          [label, ""],
          [Number(item.ideb_inicial).toFixed(1), ""],
          [Number(item.ideb_final).toFixed(1), ""],
          [`${{Number(item.variacao_ideb) >= 0 ? "+" : ""}}${{Number(item.variacao_ideb).toFixed(1)}}`, "delta"]
        ]) {{
          const cell = document.createElement("td");
          cell.textContent = value;
          cell.className = className;
          row.append(cell);
        }}
        table.append(row);
      }}

      const sources = [...new Set(rows.map((item) => item.fonte_final))];
      const sourceContainer = document.getElementById("source");
      sourceContainer.replaceChildren(document.createTextNode("Fonte: "));
      sources.forEach((url, index) => {{
        if (index > 0) sourceContainer.append(document.createTextNode(" · "));
        try {{
          const parsed = new URL(url);
          if (parsed.protocol !== "https:") throw new Error("Fonte não segura");
          const link = document.createElement("a");
          link.href = parsed.href;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.textContent = "Inep";
          sourceContainer.append(link);
        }} catch {{
          sourceContainer.append(document.createTextNode("fonte registrada nos dados"));
        }}
      }});
      document.getElementById("disclaimer").textContent =
        `${{data.source_count}} observações de entrada. Amostra agregada nacional; não representa dados de escolas ou municípios.`;
    }}

    selector.addEventListener("change", showDashboard);
    showDashboard();
  </script>
</body>
</html>"""


def create_handler(input_path: Path) -> type[BaseHTTPRequestHandler]:
    class DashboardHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path not in ("/", "/index.html"):
                self.send_error(404, "Página não encontrada")
                return

            try:
                body = render_dashboard(build_dashboard_data(input_path)).encode("utf-8")
            except (OSError, ValueError) as error:
                LOGGER.exception("Não foi possível carregar os dados para o dashboard")
                body = (
                    "<!doctype html><html lang='pt-BR'><meta charset='utf-8'>"
                    "<title>Erro no dashboard</title><h1>Não foi possível carregar os dados</h1>"
                    f"<p>{html.escape(str(error))}</p></html>"
                ).encode()
                self.send_response(500)
            else:
                self.send_response(200)

            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            LOGGER.info("%s - %s", self.address_string(), format % args)

    return DashboardHandler


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Abre um dashboard local para os dados do Ideb.")
    parser.add_argument("--input", type=Path, default=Path("data/ideb_brasil.csv"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--no-browser", action="store_true", help="Não abre o navegador automaticamente."
    )
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port deve estar entre 1 e 65535.")

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        build_dashboard_data(args.input)
        server = ThreadingHTTPServer((args.host, args.port), create_handler(args.input))
    except (OSError, ValueError) as error:
        LOGGER.error("Não foi possível iniciar o dashboard: %s", error)
        return 1

    url = f"http://{args.host}:{args.port}/"
    LOGGER.info("Dashboard disponível em %s (Ctrl+C para encerrar)", url)
    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("Encerrando dashboard")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
