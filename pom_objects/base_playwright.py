from playwright.sync_api import sync_playwright
from settings import show_browser_window


class BasePlaywright:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=not show_browser_window)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def go_to(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')

    def close_session(self):
        self.page.close()
        self.context.close()
        self.browser.close()
