from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

images = page.evaluate("""
() => Array.from(
    document.querySelectorAll("img")
).map(x => ({
    src: x.src,
    width: x.width,
    height: x.height
}))
""")

for img in images:

    if "backend-api/estuary" in img["src"]:

        print(
            img["width"],
            "x",
            img["height"],
            img["src"]
        )

input("ENTER...")