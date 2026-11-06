"""Demonstração do JC Comparativo com produção diária fictícia."""

from datetime import date, timedelta
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit


DATA_DEMO = date(2026, 10, 19)
FERIADOS_DEMO = {date(2026, 10, 16)}
# Cada linha contém operação, produção atual, produção anterior, recorde e meta.
OPERACOES = (
    ("Aurora", 51800, 46300, 62000, 50000),
    ("Horizonte", 39750, 42100, 51000, 42000),
    ("Vértice", 63500, 57000, 67500, 60000),
    ("Estrela", 27900, 25100, 33800, 30000),
)
REFERENCIAS = {"recorde": (3, "Recorde"), "meta": (4, "Meta")}


def dia_util_anterior(data, feriados):
    anterior = data - timedelta(days=1)
    while anterior.weekday() >= 5 or anterior in feriados:
        anterior -= timedelta(days=1)
    return anterior


def variacao(atual, base):
    return atual - base, (atual - base) / base * 100 if base else None


def reais(valor):
    return "R$ " + f"{valor:,.2f}".translate(str.maketrans(",.", ".,"))


def comparacao(atual, base):
    diferenca, percentual = variacao(atual, base)
    classe = "alta" if diferenca >= 0 else "queda"
    sinal = "+" if diferenca >= 0 else "−"
    valor = sinal + reais(abs(diferenca))
    taxa = f" ({percentual:+.1f}%)".replace(".", ",") if percentual is not None else ""
    return f'<span class="{classe}">{valor}{taxa}</span>'


def painel(referencia):
    indice, rotulo = REFERENCIAS.get(referencia, REFERENCIAS["recorde"])
    anterior = dia_util_anterior(DATA_DEMO, FERIADOS_DEMO)
    linhas = []
    for operacao in OPERACOES:
        nome, atual, base, *_ = operacao
        alvo = operacao[indice]
        linhas.append(
            f"<tr><th scope='row'>{escape(nome)}</th><td>{reais(atual)}</td>"
            f"<td>{reais(base)}</td><td>{comparacao(atual, base)}</td>"
            f"<td>{reais(alvo)}</td><td>{comparacao(atual, alvo)}</td></tr>"
        )
    atual_total = sum(op[1] for op in OPERACOES)
    anterior_total = sum(op[2] for op in OPERACOES)
    ref_total = sum(op[indice] for op in OPERACOES)
    opcoes = "".join(
        f'<option value="{chave}" {"selected" if indice == i else ""}>{nome}</option>'
        for chave, (i, nome) in REFERENCIAS.items()
    )
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>JC Comparativo | Demonstração</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#eff4fa;color:#152638;font:16px system-ui,sans-serif}}
main{{max-width:1080px;margin:auto;padding:36px 20px}}h1{{margin:4px 0;font-size:2.5rem}}p{{line-height:1.5}}
.tag{{color:#185485;font-weight:700}}.cards{{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}}
article{{flex:1;min-width:200px;padding:16px;background:white;border:1px solid #ccd9e5;border-radius:10px}}
article strong{{display:block;font-size:1.55rem;margin-top:5px}}form{{display:flex;align-items:center;flex-wrap:wrap;gap:10px}}
button,select{{font:inherit;border:1px solid #8ba0b5;border-radius:6px;padding:6px 10px}}button{{background:#185485;color:white;cursor:pointer}}
.scroll{{overflow:auto;background:white;border:1px solid #ccd9e5;border-radius:10px;margin-top:16px}}
table{{border-collapse:collapse;width:100%;white-space:nowrap}}th,td{{padding:13px;text-align:right;border-bottom:1px solid #dce5ef}}
th:first-child{{text-align:left}}thead,tfoot{{background:#e0ebf5}}.alta{{color:#166534}}.queda{{color:#a02127}}
</style>
</head>
<body><main>
<div class="tag">DEMONSTRAÇÃO · DADOS FICTÍCIOS</div>
<h1>JC Comparativo</h1>
<p>Produção de {DATA_DEMO:%d/%m/%Y} comparada com o dia útil anterior ({anterior:%d/%m/%Y}) e com a referência escolhida.</p>
<div class="cards">
<article>Produção do dia<strong>{reais(atual_total)}</strong></article>
<article>Variação vs. dia útil anterior<strong>{comparacao(atual_total, anterior_total)}</strong></article>
<article>Variação vs. {rotulo.lower()}<strong>{comparacao(atual_total, ref_total)}</strong></article>
</div>
<form action="/"><label for="referencia">Referência</label><select name="referencia" id="referencia">{opcoes}</select>
<button type="submit">Aplicar</button></form>
<div class="scroll"><table aria-label="Comparativo de produção por operação">
<thead><tr><th scope="col">Operação</th><th scope="col">Produção do dia</th><th scope="col">Dia útil anterior</th>
<th scope="col">Variação</th><th scope="col">{rotulo}</th><th scope="col">Diferença vs. {rotulo.lower()}</th></tr></thead>
<tbody>{''.join(linhas)}</tbody>
<tfoot><tr><th scope="row">Total</th><td>{reais(atual_total)}</td><td>{reais(anterior_total)}</td>
<td>{comparacao(atual_total, anterior_total)}</td><td>{reais(ref_total)}</td><td>{comparacao(atual_total, ref_total)}</td></tr></tfoot>
</table></div>
<p>O calendário fictício inclui um feriado em 16/10. Por isso, a comparação usa 15/10 como dia útil anterior.</p>
</main></body></html>"""


class PainelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path != "/":
            self.send_error(404)
            return
        referencia = parse_qs(url.query).get("referencia", ["recorde"])[0]
        conteudo = painel(referencia).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)


if __name__ == "__main__":
    with HTTPServer(("127.0.0.1", 8000), PainelHandler) as servidor:
        print("Abra http://127.0.0.1:8000 no navegador. Pressione Ctrl+C para encerrar.")
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            pass
