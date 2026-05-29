from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    print("\n=== TABS ===\n")

    for context in browser.contexts:
        for page in context.pages:
            print(page.title())
            print(page.url)
            print("-" * 50)