from assistant.cdp import ChromeCDP
import os

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

print("CONNECTED")

test_file = r"g:\_jabber-assistant\test.png"

if not os.path.exists(test_file):
    print("FILE NOT FOUND:", test_file)
    input()
    raise SystemExit

with page.expect_file_chooser() as fc:
    page.keyboard.press("Control+U")

chooser = fc.value

print("FILE CHOOSER FOUND")

chooser.set_files(test_file)

print("FILE UPLOADED")

input("ENTER...")