from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

page.locator("#composer-plus-btn").click()

page.locator("#upload-photos").set_input_files(
    r"g:\_jabber-assistant\test.png"
)

page.wait_for_timeout(1000)

page.locator("#prompt-textarea").click()

page.keyboard.type("Что изображено на картинке?")

page.locator("#composer-submit-button").click()

print("SENT")

input("ENTER...")