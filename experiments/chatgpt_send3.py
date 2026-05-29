from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

editor = page.locator("[contenteditable='true']").first

editor.click()

page.keyboard.type("TEST_FROM_CDP")

page.keyboard.press("Enter")

print("SENT")