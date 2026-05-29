from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    jabber = None

    for context in browser.contexts:
        for page in context.pages:

            if "chat.jabber.ru" in page.url:
                jabber = page
                break

    if not jabber:
        raise Exception("Jabber tab not found")

    print("TITLE:", jabber.title())
    print()

    print(jabber.locator("body").inner_text()[:5000])