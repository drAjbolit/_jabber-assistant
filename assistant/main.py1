import time
import os
import requests
import tempfile

from assistant.cdp import ChromeCDP
from assistant.jabber import Jabber
from assistant.chatgpt import ChatGPT
from assistant.ftp_upload import upload_file
from assistant.ws_server import WSServer


def is_image_url(text):

    text = text.lower()

    return (
        text.startswith("http")
        and (
            ".png" in text
            or ".jpg" in text
            or ".jpeg" in text
            or ".webp" in text
        )
    )


def main():

    ws = WSServer()
    ws.start()

    cdp = ChromeCDP()
    cdp.connect()

    jabber_page = cdp.find_page(
        "chat.jabber.ru"
    )

    chatgpt_page = cdp.find_page(
        "chatgpt.com"
    )

    if not jabber_page:
        print(
            "Jabber page not found"
        )
        return

    if not chatgpt_page:
        print(
            "ChatGPT page not found"
        )
        return

    jabber = Jabber(
        jabber_page
    )

    chatgpt = ChatGPT(
        chatgpt_page
    )

    print(
        "WS MODE STARTED"
    )

    while True:

        try:

            events = (
                ws.get_events()
            )

            for event in events:

                event_type = (
                    event.get(
                        "type"
                    )
                )

                if (
                    event_type
                    !=
                    "jabber_message"
                ):
                    continue

                body = (
                    event.get(
                        "text",
                        ""
                    )
                    .strip()
                )

                if not body:
                    continue

                print(
                    "[RECV]",
                    body
                )

                try:

                    if is_image_url(
                        body
                    ):

                        jabber.send_message(
                            "📷 Фото получено. Анализирую..."
                        )

                        print(
                            "[IMAGE RECEIVED]"
                        )

                        tmp = tempfile.NamedTemporaryFile(
                            suffix=".png",
                            delete=False
                        )

                        try:

                            r = requests.get(
                                body,
                                timeout=30
                            )

                            r.raise_for_status()

                            with open(
                                tmp.name,
                                "wb"
                            ) as f:

                                f.write(
                                    r.content
                                )

                            print(
                                "[IMAGE]",
                                tmp.name
                            )

                            answer = (
                                chatgpt.ask_image(
                                    tmp.name
                                )
                            )

                        finally:

                            try:
                                os.unlink(
                                    tmp.name
                                )
                            except:
                                pass

                    else:

                        before_images = (
                            chatgpt.get_image_ids()
                        )

                        answer = (
                            chatgpt.ask(
                                body
                            )
                        )

                        after_images = (
                            chatgpt.get_image_ids()
                        )

                        new_images = (
                            after_images
                            -
                            before_images
                        )

                        if new_images:

                            print(
                                "[NEW IMAGE]",
                                new_images
                            )

                            image_path = (
                                "generated.png"
                            )

                            if (
                                chatgpt.save_last_generated_image(
                                    image_path
                                )
                            ):

                                url = upload_file(
                                    image_path
                                )

                                jabber.send_message(
                                    url
                                )

                                print(
                                    "[IMAGE SENT]",
                                    url
                                )

                                try:
                                    os.unlink(
                                        image_path
                                    )
                                except:
                                    pass

                    print(
                        "[GPT]",
                        answer[:200]
                    )

                    jabber.send_message(
                        answer
                    )

                    print(
                        "[SEND]",
                        answer[:200]
                    )

                except Exception as e:

                    print(
                        "GPT ERROR:",
                        e
                    )

            time.sleep(
                0.05
            )

        except Exception as e:

            print(
                "MAIN LOOP ERROR:",
                e
            )

            time.sleep(
                1
            )


if __name__ == "__main__":
    main()