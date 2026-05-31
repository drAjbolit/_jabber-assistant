from assistant.cdp import ChromeCDP
from assistant.chatgpt import ChatGPT
from assistant.ftp_upload import upload_file

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page(
    "chatgpt.com"
)

gpt = ChatGPT(
    page
)

ok = gpt.save_last_generated_image(
    "last.png"
)

if not ok:

    print(
        "IMAGE NOT FOUND"
    )

    raise SystemExit

url = upload_file(
    "last.png"
)

print(
    "URL:"
)

print(
    url
)

input(
    "ENTER..."
)