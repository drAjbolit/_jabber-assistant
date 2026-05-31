from assistant.cdp import ChromeCDP
from assistant.chatgpt import ChatGPT

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page(
    "chatgpt.com"
)

gpt = ChatGPT(
    page
)

print(
    gpt.get_image_ids()
)

input(
    "ENTER..."
)