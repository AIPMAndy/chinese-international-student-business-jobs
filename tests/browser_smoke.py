#!/usr/bin/env python3
"""Real Chromium smoke checks for the source-built GitHub Pages handbook."""
from __future__ import annotations

import functools
import json
import os
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
assert (DIST / "index.html").exists(), "Run npm run build before browser QA"
assert (DIST / "downloads/business-careers-guide.pdf").read_bytes()[:5] == b"%PDF-", "PDF download is missing"

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

handler = functools.partial(QuietHandler, directory=str(DIST))
server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}"
artifact = ROOT / "artifacts" / "browser-smoke"
artifact.mkdir(parents=True, exist_ok=True)
summary = []

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        for width in (360, 390, 1280):
            page = browser.new_page(viewport={"width": width, "height": 820})
            page.goto(base, wait_until="networkidle")
            assert page.locator("h1").count() == 1 and "岗位证据" in page.locator("h1").inner_text()
            assert page.locator('link[rel="canonical"]').get_attribute("href") == "https://aipmandy.github.io/chinese-international-student-business-jobs/"
            ld = json.loads(page.locator('script[type="application/ld+json"]').first.inner_text())
            assert ld["@type"] == "WebPage" and ld["publisher"]["url"] == "https://www.a6no1.cn/"

            if width <= 390:
                menu = page.locator(".menu-button")
                menu.click()
                assert menu.get_attribute("aria-expanded") == "true"
                assert page.locator("#main-nav").is_visible()
                menu.click()
                assert menu.get_attribute("aria-expanded") == "false"

            finance = page.locator('[data-filter="finance"]')
            finance.click()
            assert finance.get_attribute("aria-pressed") == "true"
            assert page.locator(".route:visible").count() == 1
            page.locator('[data-filter="all"]').click()
            assert page.locator(".route:visible").count() == 6

            search = page.locator("#guide-search")
            clear = page.locator("#clear-guide-search")
            assert clear.is_disabled()
            search.fill("德国")
            page.wait_for_timeout(250)
            assert page.locator("#search-results li").count() > 0
            assert clear.is_enabled()
            clear.click()
            assert search.input_value() == ""
            assert page.locator("#search-results li").count() == 0
            assert clear.is_disabled()
            assert "可搜索" in page.locator("#search-status").inner_text()

            search.fill("zzzz-no-document-match-123")
            page.wait_for_timeout(250)
            assert "没有匹配" in page.locator("#search-status").inner_text()
            clear.click()

            page.evaluate("""() => Object.defineProperty(navigator,'clipboard',{
              configurable:true,value:{writeText:async()=>{throw Error('denied')}}
            })""")
            page.locator("#copy-wechat").click()
            assert "请手动复制" in page.locator("#copy-status").inner_text()

            assert page.locator('a[href="https://metaver.vip/services"]').count() >= 1
            contact = page.locator(".contact")
            heading_color = contact.locator("h3").evaluate("el => getComputedStyle(el).color")
            assert heading_color == "rgb(255, 255, 255)", heading_color
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), f"Horizontal overflow at {width}px"

            page.screenshot(path=str(artifact / f"homepage-{width}.png"), full_page=True)
            summary.append({"viewport": width, "search": "pass", "filters": "pass", "menu": "pass", "contact": "pass", "overflow": "pass"})
            page.close()
        browser.close()
finally:
    server.shutdown()

print(json.dumps({"status":"pass","results":summary}, ensure_ascii=False))
