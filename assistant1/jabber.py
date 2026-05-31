class Jabber:

    def __init__(
        self,
        page
    ):
        self.page = page

    def send_message(
        self,
        text
    ):

        textareas = (
            self.page.locator(
                "textarea"
            )
        )

        count = (
            textareas.count()
        )

        for i in range(
            count
        ):

            try:

                textarea = (
                    textareas.nth(i)
                )

                if not (
                    textarea.is_visible()
                ):
                    continue

                textarea.click()

                textarea.fill(
                    text
                )

                textarea.press(
                    "Enter"
                )

                print(
                    "[JABBER SEND OK]"
                )

                return

            except Exception as e:

                print(
                    "[TEXTAREA SKIP]",
                    e
                )

        raise Exception(
            "Visible textarea not found"
        )