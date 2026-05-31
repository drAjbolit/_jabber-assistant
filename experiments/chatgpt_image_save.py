from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page(
    "chatgpt.com"
)

result = page.evaluate("""
async () => {

    const imgs = Array.from(
        document.querySelectorAll("img")
    );

    const target = imgs.find(
        x =>
            x.src.includes(
                "backend-api/estuary"
            )
            &&
            x.width >= 400
    );

    if (!target)
        return null;

    const response =
        await fetch(
            target.src
        );

    const blob =
        await response.blob();

    const reader =
        new FileReader();

    return await new Promise(
        resolve => {

            reader.onload =
                () =>
                    resolve(
                        reader.result
                    );

            reader.readAsDataURL(
                blob
            );
        }
    );
}
""")

if not result:

    print("IMAGE NOT FOUND")
    input()
    raise SystemExit

prefix = "base64,"

pos = result.find(prefix)

data = result[
    pos + len(prefix):
]

import base64

with open(
    "cat.png",
    "wb"
) as f:

    f.write(
        base64.b64decode(
            data
        )
    )

print(
    "SAVED cat.png"
)

input("ENTER...")