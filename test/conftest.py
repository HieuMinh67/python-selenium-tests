import pytest
import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection

browsers = {
    "firefox": {
        "browserName": "chrome",
        "version": "80.0_VNC",
        "enableVNC": True,
        "enableVideo": True
    },
    "chrome": {
        "browserName": "firefox",
        "version": "72.0",
        "enableVNC": True,
        "enableVideo": True
    },
}

SELENOID_HOST = os.getenv("SELENOID_HOST", "localhost")
BROWSER_NAME = os.getenv("BROWSER", "firefox")
USERNAME = os.getenv("USERNAME", "standard_user")
ACCESS_KEY = os.getenv("ACCESS_KEY", "secret_sauce")


@pytest.fixture(scope="function")
def driver(request):
    # if the assignment below does not make sense to you please read up on object assignments.
    # The point is to make a copy and not mess with the original test spec.
    desired_caps = dict()
    desired_caps.update(browsers[BROWSER_NAME])
    test_name = request.node.name

    selenium_endpoint = f'http://{USERNAME}:{ACCESS_KEY}@{SELENOID_HOST}:4444/wd/hub'

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor, desired_capabilities=desired_caps, keep_alive=True
    )

    # This is specifically for SauceLabs plugin.
    # In case test fails after selenium session creation having this here will help track it down.
    # creates one file per test non ideal but xdist is awful
    if browser is not None:
        print(
            "SauceOnDemandSessionID={} job-name={}".format(
                browser.session_id, test_name
            )
        )
    else:
        raise WebDriverException("Never created!")

    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
