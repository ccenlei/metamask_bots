#!/usr/bin/python3

from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from wallet.bots_error import BotsError, NoElementFoundException


# you can find it by 'chrome://version/'
user_data_dir = '/Users/coushi/Library/Application Support/Google/Chrome'


def wait_page(driver: WebDriver, xpath: str, seconds=10):
    wait = WebDriverWait(driver, seconds)
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


def wrapper_find_element(driver: WebDriver, xpath: str, seconds=10) -> WebElement:
    wait_page(driver, xpath, seconds)
    return driver.find_element(By.XPATH, xpath)


def wrapper_find_elements(driver: WebDriver, xpath: str, seconds=10) -> List[WebElement]:
    wait_page(driver, xpath, seconds)
    return driver.find_elements(By.XPATH, xpath)


def lazy_click(element: WebElement, seconds=1):
    time.sleep(seconds)
    element.click()


class WalletOperator:

    def __init__(self) -> None:
        # set metamask extension path
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=' + user_data_dir)
        options.add_argument(
            '--disable-features=IsolateOrigins,site-per-process')
        options.add_argument('--disable-lava-moat')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        # =======if you want chrome not to load pictures, open belows.======= #
        # prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
        # options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

    def wallet_quit(self) -> None:
        self.driver.quit()

    def wallet_driver(self) -> WebDriver:
        return self.driver

    def wallet_open(self, password: str) -> WebDriver:
        print('start to open wallet.')
        # open metamask extension
        self.driver.get(
            'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        wait_page(self.driver, '//input[@id="password"]')
        # open metamask wallet
        password_input = wrapper_find_element(
            self.driver, '//input[@id="password"]')
        password_input.clear()
        password_input.send_keys(password)
        unlock_button = wrapper_find_element(
            self.driver, '//button[@data-testid="unlock-submit"]')
        unlock_button.click()
        wait_page(
            self.driver, '//button[@data-testid="address-copy-button-text"]')
        return self.driver

    def wallet_network_change(self, network: str) -> WebDriver:
        print('start to change network.')
        network_button = wrapper_find_element(
            self.driver, '//button[@data-testid="network-display"]')
        network_button.click()
        network_xpath = f'//div[@data-original-title="{network}"]'
        print(network_xpath)
        try:
            network_div = wrapper_find_element(self.driver, network_xpath)
            network_div.click()
            time.sleep(1)
            return self.driver
        except Exception as err:
            print('network error:', err)
            raise NoElementFoundException(
                BotsError.ERROR_NO_NETWORK.value, network)

    def wallet_account_change(self, account: str) -> WebDriver:
        print('start to change account.')
        address_span = wrapper_find_element(
            self.driver, '//span[@class="box mm-text mm-text--body-md mm-text--font-weight-bold mm-text--ellipsis box--flex-direction-row box--color-text-default"]')
        address_span.click()
        spans = wrapper_find_elements(
            self.driver, '//span[@class="box mm-text mm-text--inherit mm-text--ellipsis box--flex-direction-row box--color-text-default"]')
        for span in spans:
            # if you want to directly get current element's subElement, you need a '.' before '//'
            account_text = span.text
            if account == account_text:
                span.click()
                time.sleep(1)
                return self.driver
        # throw error
        raise NoElementFoundException(
            BotsError.ERROR_NO_ACCOUNT.value, account)

    def wallet_confirm(self, pre_index: int) -> WebDriver:
        print('start to confirm transaction.')
        # sometime metamask confirm-popup loads slowly, we should wait some seconds better.
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(
            'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html')
        confirm_button_path = '//button[@class="button btn--rounded btn-primary page-container__footer-button"]'
        confirm_button = wrapper_find_element(self.driver, confirm_button_path)
        confirm_button.click()
        wait_page(self.driver, '//li[@data-testid="home__activity-tab"]')
        '''
            for some unknown reason what caused such error:
                Message: javascript error: LavaMoat - property "open" of globalThis is inaccessible under scuttling mode
            when we opened wallet we need to exit current extension page
        '''
        self.driver.get('https://www.google.com/')
        self.driver.switch_to.window(self.driver.window_handles[pre_index])
        return self.driver

    def wallet_enable(self, pre_index: int) -> WebDriver:
        print('start to enable coins spends.')
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(
            'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html')
        max_ele = wrapper_find_element(
            self.driver, '//button[contains(text(),"最大")]')
        max_ele.click()
        next_ele = wrapper_find_element(
            self.driver, '//button[contains(text(),"下一步")]')
        next_ele.click()
        enable_ele = wrapper_find_element(
            self.driver, '//button[contains(text(),"批准")]')
        enable_ele.click()
        wait_page(self.driver, '//li[@data-testid="home__activity-tab"]')
        '''
            for some unknown reason what caused such error:
                Message: javascript error: LavaMoat - property "open" of globalThis is inaccessible under scuttling mode
            when we opened wallet we need to exit current extension page
        '''
        self.driver.get('https://www.google.com/')
        self.driver.switch_to.window(self.driver.window_handles[pre_index])
        return self.driver

    def wallet_connect(self, pre_index: int) -> WebDriver:
        print('start to connect website.')
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(
            'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html')
        next_ele = wrapper_find_element(
            self.driver, '//button[contains(text(),"下一步")]')
        next_ele.click()
        enable_ele = wrapper_find_element(
            self.driver, '//button[contains(text(),"连接")]')
        enable_ele.click()
        wait_page(self.driver, '//li[@data-testid="home__activity-tab"]')
        '''
            for some unknown reason what caused such error:
                Message: javascript error: LavaMoat - property "open" of globalThis is inaccessible under scuttling mode
            when we opened wallet we need to exit current extension page
        '''
        self.driver.get('https://www.google.com/')
        self.driver.switch_to.window(self.driver.window_handles[pre_index])
        return self.driver

    def wallet_disconnect(self, pre_index: int, site: str) -> WebDriver:
        print('start to disconnect website.')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(
            'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        option_ele = wrapper_find_element(
            self.driver, '//span[@class="box mm-icon mm-icon--size-sm box--display-inline-block box--flex-direction-row box--color-inherit"]')
        option_ele.click()
        connected_sites_ele = wrapper_find_element(
            self.driver, '//div[contains(text(),"已连接的网站")]')
        connected_sites_ele.click()
        site_eles = wrapper_find_elements(
            self.driver, '//div[@class="connected-sites-list__content-row"]')
        for site_ele in site_eles:
            site_text = site_ele.find_element(
                By.XPATH, './/bdi[@dir="ltr"]').text
            if site == site_text:
                a_ele = site_ele.find_element(By.XPATH, './/a[@role="button"]')
                lazy_click(a_ele)
                button_ele = wrapper_find_element(
                    self.driver, '//button[contains(text(),"断开连接")]')
                lazy_click(button_ele)
                time.sleep(3)
                break
        '''
            for some unknown reason what caused such error:
                Message: javascript error: LavaMoat - property "open" of globalThis is inaccessible under scuttling mode
            when we opened wallet we need to exit current extension page
        '''
        self.driver.get('https://www.google.com/')
        self.driver.switch_to.window(self.driver.window_handles[pre_index])
        return self.driver

    def wallet_lock(self, pre_index: int) -> None:
        print('start to lock wallet.')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get(
            'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        option_ele = wrapper_find_element(
            self.driver, '//span[@class="box mm-icon mm-icon--size-sm box--display-inline-block box--flex-direction-row box--color-inherit"]')
        option_ele.click()
        lock_ele = wrapper_find_element(
            self.driver, '//div[contains(text(),"Lock MetaMask")]')
        lock_ele.click()
        wait_page(self.driver, '//input[@id="password"]')
        self.driver.get('https://www.google.com/')
        self.driver.switch_to.window(self.driver.window_handles[pre_index])
