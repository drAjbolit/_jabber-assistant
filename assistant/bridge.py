class Bridge:

    def __init__(self, jabber, chatgpt):
        self.jabber = jabber
        self.chatgpt = chatgpt

    def process_xml(self, xml):
        answer = self.chatgpt.ask(
            "Incoming XMPP message:\n\n" + xml
        )
        self.jabber.send_message(
            answer[:3000]
        )
