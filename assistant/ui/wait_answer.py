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

    wait_response_finished(
        page,
        old_ids
    )

    answer = get_last_answer(
        page
    )

    print(
        "GPT ANSWER:"
    )

    print(
        answer
    )

    return answer