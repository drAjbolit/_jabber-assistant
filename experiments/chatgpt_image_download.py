from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page(
    "chatgpt.com"
)

if not page:
    print(
        "ChatGPT page not found"
    )
    raise SystemExit

url = (
    "https://chatgpt.com/backend-api/estuary/content?"
    "id=file_000000005e0871f5a88c0c26c444139c"
    "&ts=494470"
    "&p=fs"
    "&cid=1"
    "&sig=5b555a7cb3297af2e2a6a65cf6bb11acd5eca143818fd17c98ef80b568a4361c"
    "&v=0"
)

print(
    "DOWNLOADING..."
)

response = (
    page.context.request.get(
        url
    )
)

print(
    "STATUS:",
    response.status
)

print(
    "HEADERS:"
)

for k, v in (
    response.headers.items()
):
    print(
        k,
        ":",
        v
    )

if response.ok:

    data = response.body()

    with open(
        "cat.png",
        "wb"
    ) as f:

        f.write(
            data
        )

    print(
        "SAVED cat.png"
    )

    print(
        "SIZE:",
        len(data)
    )

else:

    print(
        "DOWNLOAD FAILED"
    )

input(
    "ENTER..."
)