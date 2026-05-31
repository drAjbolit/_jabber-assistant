from assistant.ui.find_input import find_input
from assistant.ui.find_send_button import find_send_button
from assistant.ui.find_upload_photos import find_upload_photos

from assistant.ui.wait_answer import wait_answer

from assistant.ui.get_image_ids import get_image_ids
from assistant.ui.save_last_generated_image import (
    save_last_generated_image
)

from assistant.ui.message_ids import (
    get_assistant_message_ids
)


class ChatGPT:

    def __init__(self, page):
        self.page = page

    def ask(self, text):

        old_ids = get_assistant_message_ids(
            self.page
        )

        editor = find_input(
            self.page
        )

        editor.click()

        editor.evaluate(
            '''
            (el, value) => {
                el.textContent = value;

                el.dispatchEvent(
                    new InputEvent(
                        "input",
                        { bubbles: true }
                    )
                );
            }
            ''',
            text
        )

        find_send_button(
            self.page
        ).click()

        return wait_answer(
            self.page,
            old_ids
        )

    def ask_image(
        self,
        image_path,
        prompt="Что изображено на картинке?"
    ):

        old_ids = get_assistant_message_ids(
            self.page
        )

        self.page.locator(
            "#composer-plus-btn"
        ).click()

        find_upload_photos(
            self.page
        ).set_input_files(
            image_path
        )

        self.page.wait_for_timeout(
            1000
        )

        editor = find_input(
            self.page
        )

        editor.click()

        editor.evaluate(
            '''
            (el, value) => {
                el.textContent = value;

                el.dispatchEvent(
                    new InputEvent(
                        "input",
                        { bubbles: true }
                    )
                );
            }
            ''',
            prompt
        )

        find_send_button(
            self.page
        ).click()

        return wait_answer(
            self.page,
            old_ids
        )

    def get_image_ids(self):
        return get_image_ids(
            self.page
        )

    def save_last_generated_image(
        self,
        output_path
    ):
        return save_last_generated_image(
            self.page,
            output_path
        )