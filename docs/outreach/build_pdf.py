r"""
Build a PDF of the bifurcation note for circulation.

Pipeline:  bifurcation-note.md  ->  (protect math)  ->  python-markdown  ->
           self-contained HTML with MathJax (tex-svg, local)  ->  headless Chrome  ->  PDF

Math (\( \) inline, \[ \] display) is shielded from the markdown pass with placeholders and
restored afterward, so MathJax sees raw TeX. Figures are referenced relatively and loaded
by Chrome from this directory.

Requirements (all present in this environment): python `markdown`, `google-chrome`, and the
local `mathjax-tex-svg.js` (fetched once from the MathJax CDN).

Run from inside docs/outreach/:  python3 build_pdf.py
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "bifurcation-note.md"
HTML = HERE / "bifurcation-note.html"
PDF = HERE / "bifurcation-note.pdf"

CSS = """
@page { size: Letter; margin: 22mm 20mm 22mm 20mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.6pt; line-height: 1.5;
       color: #1a1a1a; max-width: 100%; }
h1 { font-size: 17pt; line-height: 1.25; margin: 0 0 6pt; }
h2 { font-size: 13pt; margin: 16pt 0 4pt; border-bottom: 1px solid #ccc; padding-bottom: 2pt; }
h3 { font-size: 11.4pt; margin: 12pt 0 3pt; }
p { margin: 5pt 0; }
blockquote { margin: 8pt 0; padding: 6pt 12pt; background: #f6f6f4; border-left: 3px solid #b9b9b9;
             font-size: 9.8pt; }
ol, ul { margin: 5pt 0 5pt 0; padding-left: 22pt; }
li { margin: 2pt 0; }
code { font-family: 'DejaVu Sans Mono', Consolas, monospace; font-size: 9pt; background: #f0f0ee;
       padding: 0 2px; border-radius: 2px; }
pre { background: #f6f6f4; padding: 8pt 10pt; border-radius: 3px; overflow-x: auto; font-size: 8.6pt; }
pre code { background: none; padding: 0; }
img { max-width: 100%; height: auto; display: block; margin: 8pt auto 2pt; }
mjx-container[display="true"] { margin: 6pt 0; }
p:has(> img) + p { font-size: 9.4pt; color: #333; text-align: left; margin-top: 0; }
h2, h3 { page-break-after: avoid; }
img { page-break-inside: avoid; }
"""

MATHJAX_CFG = """
<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] },
  svg: { fontCache: 'global' },
  startup: { typeset: true }
};
</script>
<script src="mathjax-tex-svg.js" id="MathJax-script"></script>
"""


def protect_math(text):
    store = []

    def stash(m):
        store.append(m.group(0))
        return f"MATHPLACEHOLDER{len(store) - 1}ENDMATH"

    text = re.sub(r"\\\[.*?\\\]", stash, text, flags=re.DOTALL)   # display first
    text = re.sub(r"\\\(.*?\\\)", stash, text)                    # then inline
    return text, store


def restore_math(html, store):
    for i, raw in enumerate(store):
        html = html.replace(f"MATHPLACEHOLDER{i}ENDMATH", raw)
    return html


def main():
    try:
        import markdown
    except ImportError:
        sys.exit("need python 'markdown' (pip install markdown)")

    md = SRC.read_text(encoding="utf-8")
    md, store = protect_math(md)
    body = markdown.markdown(md, extensions=["extra", "sane_lists", "smarty"])
    body = restore_math(body, store)

    html = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Finite-Amplitude Onset of a Coexisting Attractor</title>"
        f"<style>{CSS}</style>{MATHJAX_CFG}</head><body>{body}</body></html>"
    )
    HTML.write_text(html, encoding="utf-8")
    print(f"  wrote {HTML.name} ({len(html)} bytes)")

    chrome = next((c for c in ("google-chrome", "google-chrome-stable", "chromium")
                   if subprocess.run(["which", c], capture_output=True).returncode == 0), None)
    if not chrome:
        sys.exit("no chrome found")

    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=25000",
        f"--print-to-pdf={PDF}", HTML.as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not PDF.exists():
        sys.exit(f"chrome failed ({r.returncode}):\n{r.stderr[-1500:]}")
    print(f"  wrote {PDF.name} ({PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
