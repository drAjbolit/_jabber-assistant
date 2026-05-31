from assistant.cdp import ChromeCDP
from assistant.chatgpt import ChatGPT

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

gpt = ChatGPT(page)

answer = gpt.ask(
    "Напиши слово TEST"
)

print(answer)