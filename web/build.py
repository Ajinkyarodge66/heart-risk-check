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
        .replace("/*I18N2*/", (web / "i18n2.js").read_text())
        .replace("/*I18N*/", (web / "i18n.js").read_text())
        .replace("/*CORE*/", core)
        .replace("/*QRLIB*/", (web / "vendor" / "qrcode.min.js").read_text()))
out = "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'\">\n<meta name=\"referrer\" content=\"no-referrer\">\n<link rel=\"manifest\" href=\"manifest.webmanifest\">\n<link rel=\"icon\" href=\"icon-192.png\" sizes=\"192x192\">\n<link rel=\"apple-touch-icon\" href=\"apple-touch-icon.png\">\n<meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n</head>\n<body>\n" + html + "\n</body>\n</html>\n"
(web / "index.html").write_text(out)
print("Wrote", web / "index.html", f"({len(out):,} bytes)")
