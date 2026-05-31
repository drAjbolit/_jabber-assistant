def get_last_answer(page):

    assistants = page.locator(
        '[data-message-author-role="assistant"]'
    )

    count = assistants.count()

    for i in range(
        count - 1,
        -1,
        -1
    ):

        try:

            text = (
                assistants
                .nth(i)
                .inner_text(
                    timeout=1000
                )
                .strip()
            )

            if text:
                return text

        except Exception:
            pass

    return ""