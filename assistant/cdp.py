from playwright.sync_api import sync_playwright


class ChromeCDP:

    CDP_URL = "http://127.0.0.1:9222"

    def connect(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.connect_over_cdp(
            self.CDP_URL
        )
        return self.browser

    def find_page(self, url_part):
        for context in self.browser.contexts:
            for page in context.pages:
                if url_part in page.url:
                    return page
        return None