from assistant.cdp import ChromeCDP
import json

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

data = page.evaluate("""
() => {

    return Array.from(
        document.querySelectorAll(
            '[data-message-author-role]'
        )
    ).map(x => ({
        role:
            x.getAttribute(
                'data-message-author-role'
            ),
        text:
            x.innerText
    }));
}
""")

with open(
    "chatgpt_dom.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )

print("DONE")