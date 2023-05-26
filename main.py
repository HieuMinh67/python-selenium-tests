import os
from time import sleep

from selenium import webdriver

SELENOID_HOST = os.getenv("SELENOID_HOST", "localhost")
BROWSER_NAME = os.getenv("BROWSER", "firefox")


# get google title with VNC session from Firefox browser
def test_firefox():
    capabilities = {
        "browserName": "firefox",
        "version": "72.0",
        "enableVNC": False,
        "enableVideo": False
    }
    firefox = webdriver.Remote(
        command_executor=f'http://{SELENOID_HOST}:4444/wd/hub',
        desired_capabilities=capabilities
    )
    firefox.get('https://www.google.com')
    print('firefox', firefox.title)
    sleep(10)
    firefox.quit()


# get google title with VNC session from Chrome browser
def test_chrome():
    capabilities = {
        "browserName": "chrome",
        "version": "80.0_VNC",
        "enableVNC": True,
        "enableVideo": False
    }
    chrome = webdriver.Remote(
        command_executor=f'http://{SELENOID_HOST}:4444/wd/hub',
        desired_capabilities=capabilities
    )
    chrome.get('https://www.google.com')
    print('chrome', chrome.title)
    sleep(10)
    chrome.quit()


if __name__ == "__main__":
    test_firefox() if BROWSER_NAME == "firefox" else test_chrome()
