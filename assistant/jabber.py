class Jabber:

    def __init__(self, page):
        self.page = page

    def send_message(self, text):
        textarea = self.page.locator("textarea").first
        textarea.fill(text)
        textarea.press("Enter")
