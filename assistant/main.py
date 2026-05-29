from assistant.cdp import ChromeCDP
from assistant.jabber import Jabber


def main():
    cdp = ChromeCDP()
    cdp.connect()

    jabber_page = cdp.find_page("chat.jabber.ru")

    if not jabber_page:
        print("JABBER: False")
        return

    print("JABBER: True")

    jabber = Jabber(jabber_page)
    jabber.send_message("Hello from assistant module")


if __name__ == "__main__":
    main()
