from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

print("TITLE:", page.title())

print("\nTEXTAREAS")
print("=" * 50)

for i, el in enumerate(page.locator("textarea").all()):
    print(i, el)

print("\nINPUTS")
print("=" * 50)

for i, el in enumerate(page.locator("input").all()):
    try:
        print(i, el.get_attribute("placeholder"))
    except:
        pass