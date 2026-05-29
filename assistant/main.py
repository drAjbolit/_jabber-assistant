from assistant.cdp import ChromeCDP
from assistant.jabber import Jabber


def main():
    cdp = ChromeCDP()
    cdp.connect()

    jabber_page = cdp.find_page("chat.jabber.ru")

    print("JABBER:", bool(jabber_page))

    if jabber_page:
        Jabber(jabber_page).send_message("Hello from assistant module")


if __name__ == "__main__":
    main()
