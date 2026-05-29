from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    jabber = None

    for context in browser.contexts:
        for page in context.pages:
            if "chat.jabber.ru" in page.url:
                jabber = page

    jabber.on(
        "console",
        lambda msg: print(
            f"[BROWSER] {msg.text}"
        )
    )

    jabber.evaluate("""
    () => {

        if (window.__jabber_assistant_installed)
            return;

        window.__jabber_assistant_installed = true;

        console.log(
            "__JABBER_ASSISTANT_READY__"
        );

        const observer =
            new MutationObserver(() => {

                console.log(
                    "__DOM_CHANGED__"
                );

            });

        observer.observe(
            document.body,
            {
                childList: true,
                subtree: true
            }
        );

    }
    """)

    print("Waiting...")

    while True:
        time.sleep(1)