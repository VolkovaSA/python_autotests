import pytest
from playwright.sync_api import sync_playwright
import logging


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(10000)  # 10 seconds
        logging.info('Browser has been started')
        yield page
        context.close()
        browser.close()
        logging.info('Browser has been closed')


@pytest.fixture(scope="function")
def set_up_browser(page):
    logging.info('Preparing browser')
    return page
