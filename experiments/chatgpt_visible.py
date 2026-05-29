cdp = ChromeCDP(
cdp.connect()

page = cdp.find_page("chatgpt.com")

print(page.locator("[contenteditable='true']").count())

for i in range(page.locator("[contenteditable='true']").count()):
    el = page.locator("[contenteditable='true']").nth(i)
    print(i, el.is_visible())
