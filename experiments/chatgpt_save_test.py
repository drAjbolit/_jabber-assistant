from assistant.cdp import ChromeCDP
from assistant.chatgpt import ChatGPT

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page(
    "chatgpt.com"
)

gpt = ChatGPT(page)

ok = gpt.save_last_generated_image(
    "last.png"
)

print(
    "RESULT:",
    ok
)

input("ENTER...")