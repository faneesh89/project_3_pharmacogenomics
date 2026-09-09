# report_generator.py
# Simple, clean HTML report for pharmacogenomics star allele results.

import os
from datetime import datetime


def generate_html_report(alleles, output_filename="output/pgx_clinical_report.html"):
    """
    alleles: dict from call_alleles() — {gene: [list of allele dicts]}
    Each allele dict has: 'allele', 'function', 'rs', 'note'
    """

    # Build table rows
    rows_html = ""
    total_alleles = 0

    for gene, allele_list in alleles.items():
        if allele_list:
            allele_names = ", ".join(a['allele'] for a in allele_list)
            functions    = ", ".join(a['function'] for a in allele_list)
            rs_numbers   = ", ".join(a['rs'] for a in allele_list)
            total_alleles += len(allele_list)
            row_class = "found"
        else:
            allele_names = "*1 (reference)"
            functions    = "normal"
            rs_numbers   = "—"
            row_class = "reference"

        rows_html += f"""
        <tr class="{row_class}">
            <td><strong>{gene}</strong></td>
            <td>{allele_names}</td>
            <td>{functions}</td>
            <td>{rs_numbers}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Pharmacogenomics Clinical Report</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        background: #f5f5f5;
        margin: 0;
        padding: 30px;
        color: #222;
    }}
    .container {{
        max-width: 900px;
        margin: 0 auto;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        overflow: hidden;
    }}
    .header {{
        background: #1F4E79;
        color: white;
        padding: 24px 30px;
    }}
    .header h1 {{ margin: 0 0 6px 0; font-size: 22px; }}
    .header p  {{ margin: 0; font-size: 13px; color: #c8dff0; }}
    .summary {{
        padding: 16px 30px;
        background: #EBF3FB;
        border-bottom: 1px solid #d0e4f5;
        font-size: 14px;
    }}
    .content {{ padding: 20px 30px; }}
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }}
    th {{
        background: #2E75B6;
        color: white;
        padding: 10px 12px;
        text-align: left;
    }}
    td {{
        padding: 9px 12px;
        border-bottom: 1px solid #e8e8e8;
        vertical-align: top;
    }}
    tr.found     {{ background: #FFF8E1; }}
    tr.reference {{ background: #F9F9F9; color: #888; }}
    tr.found:hover {{ background: #FFF3CD; }}
    .disclaimer {{
        margin: 20px 0 0 0;
        padding: 12px 16px;
        background: #FFF3E0;
        border-left: 4px solid #E65100;
        font-size: 12px;
        color: #666;
        border-radius: 0 4px 4px 0;
    }}
    .footer {{
        text-align: center;
        padding: 14px;
        font-size: 11px;
        color: #aaa;
        border-top: 1px solid #eee;
    }}
</style>
</head>
<body>
<div class="container">

    <div class="header">
        <h1>Pharmacogenomics Clinical Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="summary">
        <strong>{total_alleles}</strong> variant alleles identified across
        <strong>{len(alleles)}</strong> pharmacogenes.
        Genes showing only *1 (reference) had no known tag variants detected.
    </div>

    <div class="content">
        <table>
            <tr>
                <th>Gene</th>
                <th>Called Allele(s)</th>
                <th>Function</th>
                <th>RS Number(s)</th>
            </tr>
            {rows_html}
        </table>

        <div class="disclaimer">
            <strong>Note:</strong> This report is generated from a simplified
            pharmacogenomics pipeline covering a representative subset of
            clinically common star alleles. Results are based on variant
            matching by rs number against CPIC/PharmVar reference data.
            This is an educational/portfolio project and is NOT intended
            for clinical diagnostic use.
        </div>
    </div>

    <div class="footer">
        Pharmacogenomics Analysis Pipeline — Project 3
    </div>

</div>
</body>
</html>"""

    # Create output directory if needed
    out_dir = os.path.dirname(output_filename)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Report saved to: {output_filename}")
    return output_filename