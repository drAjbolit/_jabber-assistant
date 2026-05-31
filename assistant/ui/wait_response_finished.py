import time

from assistant.ui.message_ids import (
    get_assistant_message_ids
)


def wait_response_finished(
    page,
    old_ids
):

    print(
        "WAITING NEW ASSISTANT MESSAGE..."
    )

    while True:

        current_ids = (
            get_assistant_message_ids(
                page
            )
        )

        new_ids = (
            current_ids
            - old_ids
        )

        real_ids = {
            msg_id
            for msg_id in new_ids
            if not msg_id.startswith(
                "request-placeholder"
            )
        }

        if real_ids:

            msg_id = list(
                real_ids
            )[0]

            print(
                "NEW MESSAGE:",
                msg_id
            )

            return msg_id

        time.sleep(
            0.1
        )