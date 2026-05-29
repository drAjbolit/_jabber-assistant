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

    print("TEXTAREAS")
    print("=" * 50)

    for i, el in enumerate(jabber.locator("textarea").all()):
        print(i, el)

    print()
    print("INPUTS")
    print("=" * 50)

    for i, el in enumerate(jabber.locator("input").all()):
        try:
            print(
                i,
                el.get_attribute("type"),
                el.get_attribute("placeholder"),
            )
        except:
            pass