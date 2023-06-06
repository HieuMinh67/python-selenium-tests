import os
from time import sleep

from selenium import webdriver

SELENOID_HOST = os.getenv("SELENOID_HOST", "localhost")
BROWSER_NAME = os.getenv("BROWSER", "firefox")


# get google title with VNC session from Firefox browser
def run_firefox():
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
    sleep(5)
    firefox.quit()
    return 'https://www.google.com'


# get google title with VNC session from Chrome browser
def run_chrome():
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
    sleep(5)
    chrome.quit()
    return 'https://www.google.com'


if __name__ == "__main__":
    run_firefox() if BROWSER_NAME == "firefox" else run_chrome()
