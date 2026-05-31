from assistant.ui.get_last_answer import (
    get_last_answer
)

from assistant.ui.wait_response_finished import (
    wait_response_finished
)


def wait_answer(
    page,
    old_ids
):

    msg_id = (
        wait_response_finished(
            page,
            old_ids
        )
    )

    answer = (
        get_last_answer(
            page,
            msg_id
        )
    )

    print(
        "GPT ANSWER:"
    )

    print(
        answer
    )

    return answer