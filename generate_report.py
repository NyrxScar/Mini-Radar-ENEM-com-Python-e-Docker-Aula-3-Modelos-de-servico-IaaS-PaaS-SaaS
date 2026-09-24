import os
import subprocess
import markdown

# Read RUNBOOK.md
with open("RUNBOOK.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown to HTML
html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório Prático - Mini Radar ENEM (Aula 7)</title>
<style>
    @page {{
        size: A4;
        margin: 20mm 15mm 20mm 15mm;
        @bottom-right {{
            content: "Página " counter(page) " de " counter(pages);
            font-size: 9pt;
            font-family: Arial, sans-serif;
            color: #666;
        }}
    }}
    body {{
        font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
        line-height: 1.6;
        color: #2c3e50;
        margin: 0;
        padding: 20px;
        background-color: #ffffff;
    }}
    h1 {{
        color: #1a365d;
        border-bottom: 3px solid #2b6cb0;
        padding-bottom: 8px;
        font-size: 24pt;
        margin-top: 0;
    }}
    h2 {{
        color: #2b6cb0;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 5px;
        font-size: 16pt;
        margin-top: 25px;
        page-break-after: avoid;
    }}
    h3 {{
        color: #2d3748;
        font-size: 12pt;
        margin-top: 18px;
        page-break-after: avoid;
    }}
    p, li {{
        font-size: 10pt;
        text-align: justify;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 9.5pt;
        page-break-inside: avoid;
    }}
    th, td {{
        border: 1px solid #cbd5e0;
        padding: 8px 12px;
        text-align: left;
    }}
    th {{
        background-color: #2b6cb0;
        color: #ffffff;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #f7fafc;
    }}
    code {{
        font-family: 'Consolas', 'Courier New', monospace;
        background-color: #edf2f7;
        padding: 2px 5px;
        border-radius: 3px;
        font-size: 9pt;
        color: #c53030;
    }}
    pre {{
        background-color: #1a202c;
        color: #edf2f7;
        padding: 12px;
        border-radius: 5px;
        overflow-x: auto;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8.5pt;
        line-height: 1.4;
        page-break-inside: avoid;
    }}
    pre code {{
        background-color: transparent;
        color: inherit;
        padding: 0;
    }}
    blockquote {{
        border-left: 4px solid #3182ce;
        background-color: #ebf8ff;
        margin: 15px 0;
        padding: 10px 15px;
        color: #2b6cb0;
        font-size: 9.5pt;
    }}
    .header-box {{
        background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
        color: white;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 30px;
    }}
    .header-box h1 {{
        color: white;
        border-bottom: none;
        margin: 0 0 10px 0;
        font-size: 22pt;
    }}
    .header-box p {{
        margin: 4px 0;
        font-size: 11pt;
        color: #e2e8f0;
    }}
    .badge {{
        display: inline-block;
        background-color: #38a169;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 8.5pt;
        font-weight: bold;
    }}
</style>
</head>
<body>

<div class="header-box">
    <h1>Relatório de Atividade Prática</h1>
    <p><strong>Curso:</strong> Computação em Nuvem • Aula 7</p>
    <p><strong>Projeto:</strong> Mini Radar ENEM — Do Protótipo à Produção</p>
    <p><strong>Tópicos:</strong> Operação, Segurança, Observabilidade, Recuperação de Incidentes e Rollback</p>
    <p><strong>Ambiente:</strong> Laboratório com Docker Engine em IaaS Linux</p>
    <p><strong>Status:</strong> <span class="badge">CONCLUÍDO COM SUCESSO</span></p>
</div>

{html_body}

</body>
</html>
"""

with open("Relatorio_Atividade_Aula7_Mini_Radar_ENEM.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("HTML generated successfully.")
