def get_last_answer(
    page,
    msg_id
):

    try:

        msg = page.locator(
            f'[data-message-id="{msg_id}"]'
        )

        text = (
            msg
            .inner_text(
                timeout=5000
            )
            .strip()
        )

        print(
            "ANSWER LEN:",
            len(text)
        )

        print(
            "ANSWER END:",
            repr(
                text[-300:]
            )
        )

        return text

    except Exception as e:

        print(
            "GET ANSWER ERROR:",
            e
        )

        return ""