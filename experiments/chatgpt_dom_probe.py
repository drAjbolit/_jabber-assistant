from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

selectors = [
    "[contenteditable='true']",
    ".ProseMirror",
    "[role='textbox']",
    "textarea",
]

for s in selectors:
    loc = page.locator(s)
    print()
    print("SELECTOR:", s)
    print("COUNT:", loc.count())

    if loc.count():
        try:
            print("VISIBLE:", loc.first.is_visible())
        except Exception as e:
            print("ERR:", e)