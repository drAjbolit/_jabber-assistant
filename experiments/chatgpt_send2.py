from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

page.locator("textarea").first.click()
page.keyboard.type("TEST_FROM_CDP")
page.keyboard.press("Enter")
print("SENT")
