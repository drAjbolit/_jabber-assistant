from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

text = page.locator("main").inner_text()

with open(
    "chatgpt_page.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(text)

print("DONE")