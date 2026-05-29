from assistant.cdp import ChromeCDP
import time

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

print("Waiting 5 seconds...")

time.sleep(5)

text = page.locator("main").inner_text()

with open(
    "answer.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(text)

print("SAVED")