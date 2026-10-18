"""Build web/index.html: put the trained model, translations and model code into one self-contained page.
Run from the repository root:  python web/build.py
"""
import json
from pathlib import Path
root = Path(__file__).resolve().parent.parent
web = root / "web"
model = json.loads((root / "model" / "model_global.json").read_text())
core = (web / "core.js").read_text().replace(
    'if (typeof module !== "undefined") module.exports = { rawScore, scorePerson, contributions };', "")
html = ((web / "app_src.html").read_text()
        .replace("/*MODEL*/", json.dumps(model, separators=(",", ":")))
        .replace("/*I18N*/", (web / "i18n.js").read_text())
        .replace("/*CORE*/", core))
out = "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n</head>\n<body>\n" + html + "\n</body>\n</html>\n"
(web / "index.html").write_text(out)
print("Wrote", web / "index.html", f"({len(out):,} bytes)")
