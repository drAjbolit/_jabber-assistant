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

    result = jabber.evaluate("""
        () => {
            window.__jabber_assistant = {
                active: true,
                version: "0.1"
            };

            return window.__jabber_assistant;
        }
    """)

    print(result)