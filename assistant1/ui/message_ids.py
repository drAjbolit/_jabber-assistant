def get_assistant_message_ids(page):

    msgs = page.locator(
        '[data-message-author-role="assistant"]'
    )

    result = []

    count = msgs.count()

    for i in range(count):

        try:

            msg_id = msgs.nth(i).get_attribute(
                "data-message-id"
            )

            if msg_id:
                result.append(
                    msg_id
                )

        except Exception:
            pass

    return set(result)