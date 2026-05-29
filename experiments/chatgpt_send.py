from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

textarea = page.locator("textarea").first

textarea.fill("Напиши слово TEST")

textarea.press("Enter")

print("SENT")