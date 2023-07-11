#!/usr/bin/python3

from selenium.webdriver.common.by import By
import time

from wallet.wallet_ops import WalletOperator, lazy_click, wrapper_find_element


# https://beagleswap.xyz/
pre_index = 1


def swap_bot(op: WalletOperator, op_count=3) -> None:
    driver = op.wallet_driver()
    beagle_window = 'window.open("https://beagleswap.xyz/swap","_blank");'
    driver.execute_script(beagle_window)
    driver.switch_to.window(driver.window_handles[pre_index])
    connect_ele = wrapper_find_element(
        driver, '//div[@class="sc-3a5c8d1f-1 fQjBku"]')
    lazy_click(connect_ele)
    wallet_ele = wrapper_find_element(
        driver, '//div[contains(text(),"Metamask")]')
    lazy_click(wallet_ele)
    op.wallet_connect(pre_index)
    try:
        while op_count > 0:
            op_count -= 1
            input_from_ele = wrapper_find_element(
                driver, '//input[@class="token-amount-input _1cvvxtw5 _1cvvxtw8"]')
            input_from_ele.send_keys('0.01')
            swap_ele = wrapper_find_element(
                driver, '//button[@id="swap-button"]')
            lazy_click(swap_ele)
            # check price updated
            acc_ele = driver.find_element(
                By.XPATH, '//button[@class="sc-6e2c9a09-0 kKwAZE"]')
            if acc_ele.is_enabled():
                acc_ele.click
            # updated_eles = driver.find_elements(
            #     By.XPATH, '//div[@class="sc-c56ebc7d-0 feFKuX"]')
            # if (len(updated_eles) > 0):
            #     acc_ele = driver.find_element(
            #         By.XPATH, '//button[@class="sc-6e2c9a09-0 kKwAZE"]')
            #     acc_ele.click()
            swap_confirm_ele = wrapper_find_element(
                driver, '//button[@id="confirm-swap-or-send"]')
            swap_confirm_ele.click()
            op.wallet_confirm(pre_index)
            close_ele = wrapper_find_element(
                driver, '//button[@class="sc-6e2c9a09-0 cNwfbL"]')
            close_ele.click()
            time.sleep(1)
    except Exception as err:
        print('swap error:', err)
    finally:
        op.wallet_disconnect(pre_index, 'beagleswap.xyz')


def bot_all():
    password = input('===intput your password：')
    op = WalletOperator()
    op.wallet_open(password)
    op.wallet_account_change('Account 1')
    driver = op.wallet_network_change('Base Goerli Testnet')
    driver.get('https://www.google.com/')
    swap_bot(op)
    op.wallet_quit()


bot_all()
