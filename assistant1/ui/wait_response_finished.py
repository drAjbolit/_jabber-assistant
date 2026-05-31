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

    old_good_buttons = (
        page
        .locator(
            '[data-testid="good-response-turn-action-button"]'
        )
        .count()
    )

    print(
        f"GOOD BUTTONS BEFORE: {old_good_buttons}"
    )

    msg_id = None

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
            x
            for x in new_ids
            if not x.startswith(
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

            break

        time.sleep(
            0.1
        )

    print(
        "WAITING NEW ACTION BUTTONS..."
    )

    while True:

        try:

            current_good_buttons = (
                page
                .locator(
                    '[data-testid="good-response-turn-action-button"]'
                )
                .count()
            )

            if (
                current_good_buttons
                > old_good_buttons
            ):

                print(
                    "NEW GOOD BUTTON FOUND"
                )

                print(
                    f"GOOD BUTTONS NOW: {current_good_buttons}"
                )

                break

        except Exception:
            pass

        time.sleep(
            0.2
        )

    print(
        "RESPONSE FINISHED"
    )

    return msg_id