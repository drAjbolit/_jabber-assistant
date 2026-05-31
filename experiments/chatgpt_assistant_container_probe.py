from assistant.cdp import ChromeCDP

cdp = ChromeCDP()
cdp.connect()

page = cdp.find_page("chatgpt.com")

msgs = page.locator(
    '[data-message-author-role="assistant"]'
)

count = msgs.count()

print(
    "ASSISTANT MSG COUNT:",
    count
)

if count == 0:

    print(
        "NO ASSISTANT MESSAGES"
    )

    input()

    raise SystemExit

last = msgs.nth(
    count - 1
)

print("\n=== SELF ===\n")

try:

    print(
        last.evaluate(
            "el => el.outerHTML"
        )
    )

except Exception as e:

    print(
        "SELF ERROR:",
        e
    )

print("\n=== PARENT ===\n")

try:

    print(
        last.evaluate(
            """
            el =>
                el.parentElement
                ? el.parentElement.outerHTML
                : ""
            """
        )
    )

except Exception as e:

    print(
        "PARENT ERROR:",
        e
    )

print("\n=== GRANDPARENT ===\n")

try:

    print(
        last.evaluate(
            """
            el =>
                el.parentElement &&
                el.parentElement.parentElement
                ? el.parentElement.parentElement.outerHTML
                : ""
            """
        )
    )

except Exception as e:

    print(
        "GRANDPARENT ERROR:",
        e
    )

print("\n=== ATTRIBUTES ===\n")

try:

    attrs = last.evaluate(
        """
        el => {

            const result = {};

            for (
                const attr
                of el.attributes
            ) {

                result[
                    attr.name
                ] = attr.value;
            }

            return result;
        }
        """
    )

    print(attrs)

except Exception as e:

    print(
        "ATTR ERROR:",
        e
    )

input(
    "ENTER..."
)