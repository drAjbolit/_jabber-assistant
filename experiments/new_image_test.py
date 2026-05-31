from assistant.cdp import ChromeCDP
from assistant.chatgpt import ChatGPT

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page(
    "chatgpt.com"
)

gpt = ChatGPT(page)

before = gpt.get_image_ids()

print(
    "BEFORE:",
    before
)

input(
    "Сгенерируй новую картинку и нажми Enter..."
)

after = gpt.get_image_ids()

print(
    "AFTER:",
    after
)

print(
    "NEW:",
    after - before
)

input("ENTER...")