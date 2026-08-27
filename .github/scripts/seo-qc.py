from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

OUT = Path("_site")
BASE = os.environ.get("RENOMETRIC_BASE", "/tangxuejia")
ORIGIN = os.environ.get("RENOMETRIC_ORIGIN", "https://renometric.pages.dev")
errors: list[str] = []


def route_file(url: str) -> Path | None:
    path = unquote(urlsplit(url).path or "/")
    origin_base = urlsplit(ORIGIN).path.rstrip("/")
    if origin_base and (path == origin_base or path.startswith(origin_base + "/")):
        path = path[len(origin_base):] or "/"
    elif BASE and (path == BASE or path.startswith(BASE + "/")):
        path = path[len(BASE):] or "/"

    rel = path.lstrip("/")
    if path == "/":
        candidates = [OUT / "index.html"]
    elif path.endswith("/"):
        candidates = [OUT / rel / "index.html"]
    elif path.endswith(".html"):
        candidates = [OUT / rel]
    else:
        candidates = [OUT / rel / "index.html", OUT / (rel + ".html")]
    return next((candidate for candidate in candidates if candidate.is_file()), None)


if not OUT.exists():
    errors.append("_site directory is missing")
else:
    sitemap = OUT / "sitemap.xml"
    if not sitemap.is_file():
        errors.append("_site/sitemap.xml is missing")
        public_files: list[Path] = []
    else:
        sitemap_text = sitemap.read_text(encoding="utf-8", errors="ignore")
        sitemap_urls = re.findall(r"<loc>(.*?)</loc>", sitemap_text)
        if not sitemap_urls:
            errors.append("sitemap contains no URLs")
        public_files = []
        expected_origin = ORIGIN.rstrip("/")
        for url in sitemap_urls:
            if url.rstrip("/") == expected_origin + "/calculators/index":
                errors.append("sitemap contains duplicate calculators/index route")
            if not (url == expected_origin or url.startswith(expected_origin + "/")):
                errors.append(f"sitemap URL uses the wrong origin: {url}")
            target = route_file(url)
            if target is None:
                errors.append(f"sitemap route has no generated file: {url}")
            elif target not in public_files:
                public_files.append(target)

        robots = OUT / "robots.txt"
        if not robots.is_file():
            errors.append("_site/robots.txt is missing")
        else:
            robots_text = robots.read_text(encoding="utf-8", errors="ignore")
            expected_sitemap = expected_origin + "/sitemap.xml"
            if f"Sitemap: {expected_sitemap}" not in robots_text:
                errors.append(f"robots.txt does not point to {expected_sitemap}")
            if re.search(r"^Disallow:\\s*/\\s*$", robots_text, re.M | re.I):
                errors.append("robots.txt blocks the whole site")

    for page in public_files:
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
        if "renometric.netlify.app" in text:
            errors.append(f"{page}: contains an old deployment domain")
        if re.search(r'href=["\'][^"\']*/guides/[^"\']+\.html(?:[?#][^"\']*)?["\']', text, re.I):
            errors.append(f"{page}: guide link contains .html")
        if re.search(r'href=["\'][^"\']*/calculators/[^"\']+\.html(?:[?#][^"\']*)?["\']', text, re.I):
            errors.append(f"{page}: calculator link contains .html")

        for href in re.findall(r'''<a\b[^>]+href=["']([^"']+)''', text, re.I):
            if href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            parsed = urlsplit(href)
            if parsed.scheme and parsed.scheme not in ("http", "https"):
                continue
            if parsed.netloc and parsed.netloc not in ("renometric.pages.dev", "tangxuejia.github.io"):
                continue
            target = route_file(href)
            if target is None:
                errors.append(f"{page}: broken internal link {href}")

        script_open_count = len(re.findall(r"<script\b", text, re.I))
        script_close_count = len(re.findall(r"</script\s*>", text, re.I))
        if script_open_count != script_close_count:
            errors.append(f"{page}: unbalanced script tags ({script_open_count} open, {script_close_count} close)")
        visible_text = re.sub(r"<script\b[^>]*>.*?</script\s*>", " ", text, flags=re.S | re.I)
        visible_text = re.sub(r"<style\b[^>]*>.*?</style\s*>", " ", visible_text, flags=re.S | re.I)
        visible_text = re.sub(r"<[^>]+>", " ", visible_text)
        if re.search(r"\bfunction\s+(?:setUnit|copyPlan|saveProject)\s*\(", visible_text):
            errors.append(f"{page}: JavaScript function is visible as page text")
        if re.search(r"\bdocument\.getElementById\b|\blocalStorage\.(?:getItem|setItem)\b", visible_text):
            errors.append(f"{page}: raw JavaScript expression is visible as page text")

if errors:
    print("SEO QC FAILED")
    print("\n".join(f"- {item}" for item in errors))
    sys.exit(1)

print(f"SEO QC passed: {len(public_files)} sitemap pages checked")
