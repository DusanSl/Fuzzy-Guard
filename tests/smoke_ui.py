"""Ručni Playwright smoke test za UI.

Nije deo pytest kolekcije jer zahteva pokrenut server i instaliran browser.

    python main.py            # u drugom terminalu
    python tests/smoke_ui.py
"""

import os
import sys

from playwright.sync_api import sync_playwright

URL = os.environ.get("FUZZY_GUARD_URL", "http://127.0.0.1:5000")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")

        assert page.get_by_role("textbox", name="Message").count() == 1

        page.click('[data-uzorak="prevara"]')
        page.click('#pokreni-dugme')
        page.wait_for_function(
            "() => document.getElementById('status') && !document.getElementById('status').hidden"
        )
        page.wait_for_timeout(800)

        kategorija = page.inner_text("#status-tekst").upper()
        skor = page.inner_text("#skor-broj")
        assert "SPAM" in kategorija or "PREVARA" in kategorija, (kategorija, skor)
        assert page.locator("#spektar path").count() >= 6

        page.click('[data-pogled="ulazi"]')
        assert page.locator("#pogled-sadrzaj .ulaz").count() == 5

        page.click('[data-pogled="pravila"]')
        assert page.locator("#pogled-sadrzaj .pravilo").count() >= 1

        page.click('[data-pogled="zasto"]')
        assert page.locator(".leksikon-status").count() == 1
        assert "(auto)" in page.locator(".leksikon-status").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")

        page.click('[data-otvori-metod]')
        assert page.locator("#metod").is_visible()
        assert page.locator("#spektar-metod path").count() >= 6

        browser.close()
        print(f"UI smoke OK: {kategorija} {skor}")


if __name__ == "__main__":
    sys.exit(main())
