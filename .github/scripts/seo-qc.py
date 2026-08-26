from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

OUT = Path("_site")
BASE = os.environ.get("RENOMETRIC_BASE", "")
errors: list[str] = []

if not OUT.exists():
    errors.append("_site directory is missing")
else:
    html_files = sorted(OUT.rglob("*.html"))
    if not html_files:
        errors.append("no HTML pages were generated")

    for page in html_files:
        text = page.read_text(encoding="utf-8", errors="ignore")
        title = re.search(r"<title[^>]*>.*?</title>", text, re.S | re.I)
        description = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']+["\']', text, re.S | re.I)
        canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']', text, re.S | re.I)
        if not title:
            errors.append(f"{page}: missing title")
        if not description:
            errors.append(f"{page}: missing meta description")
        if not canonical:
            errors.append(f"{page}: missing canonical")
        if "renometric.netlify.app" in text or "tangxuejia.github.io/tangxuejia" in text:
            errors.append(f"{page}: contains an old deployment domain")
        if re.search(r'href=["\'][^"\']*/guides/[^"\']+\.html(?:[?#][^"\']*)?["\']', text, re.I):
            errors.append(f"{page}: guide link contains .html")

        for href in re.findall(r"<a\b[^>]+href=["']([^"']+)", text, re.I):
            if href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            parsed = urlsplit(href)
            if parsed.scheme and parsed.scheme not in ("http", "https"):
                continue
            if parsed.netloc and parsed.netloc not in ("renometric.pages.dev", "tangxuejia.github.io"):
                continue

            path = unquote(parsed.path or "/")
            if BASE and (path == BASE or path.startswith(BASE + "/")):
                path = path[len(BASE):] or "/"
            if path == "/":
                candidates = [OUT / "index.html"]
            elif path.endswith("/"):
                candidates = [OUT / path.lstrip("/") / "index.html"]
            elif path.endswith(".html"):
                candidates = [OUT / path.lstrip("/")]
            else:
                candidates = [
                    OUT / path.lstrip("/") / "index.html",
                    OUT / (path.lstrip("/") + ".html"),
                ]
            if not any(candidate.is_file() for candidate in candidates):
                errors.append(f"{page}: broken internal link {href}")

if errors:
    print("SEO QC FAILED")
    print("\n".join(f"- {item}" for item in errors))
    sys.exit(1)

print(f"SEO QC passed: {len(list(OUT.rglob('*.html')))} HTML files checked")
