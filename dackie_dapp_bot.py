#!/usr/bin/python3

from selenium.webdriver.common.by import By
import time

from wallet.wallet_ops import WalletOperator, lazy_click, wrapper_find_element


# https://www.dackieswap.xyz/swap?chain=base
pre_index = 1


def dackie_swap(op: WalletOperator):
    driver = op.wallet_driver()
    print("dackie enable.")
    enable_button_ele = wrapper_find_element(
        driver, '//button[@class="sc-a09a241a-0 kGXwdN"]')
    enable_button_ele.click()
    op.wallet_enable(pre_index, True)
    time.sleep(10)
    print("dackie swap.")
    swap_button_ele = wrapper_find_element(
        driver, '//button[@id="swap-button"]')
    swap_button_ele.click()
    confirm_button_ele = wrapper_find_element(
        driver, '//button[@id="confirm-swap-or-send"]')
    confirm_button_ele.click()
    op.wallet_confirm(pre_index, True)
    time.sleep(10)
    close_button_ele = wrapper_find_element(
        driver, '//button[@class="sc-a09a241a-0 dIEdsM"]')
    close_button_ele.click()
    print("dackie change.")
    button_change_ele = wrapper_find_element(
        driver, '//button[@class="sc-a09a241a-0 lcKOKl sc-e6c6e658-0 sc-ce351f2d-0 lbAREi ikmIEZ"]')
    button_change_ele.click()


def bot_swap(op: WalletOperator):
    driver = op.wallet_driver()
    input_ele = wrapper_find_element(
        driver, '//input[@class="token-amount-input _1cvvxtw3 _1cvvxtw8"]')
    input_ele.clear
    input_ele.send_keys('1002.1')
    dackie_swap(op)
    max_button_ele = wrapper_find_element(
        driver, '//button[contains(text(),"Max")]')
    max_button_ele.click()
    dackie_swap(op)


def bot_dackie():
    password = input('===intput your password：')
    op = WalletOperator()
    op.wallet_open(password)
    op.wallet_account_change('Account 1')
    driver = op.wallet_network_change('Base')
    driver.get('https://www.google.com/')
    driver = op.wallet_driver()
    dackie_window = 'window.open("https://www.dackieswap.xyz/swap?chain=base&outputCurrency=0xEB466342C4d449BC9f53A865D5Cb90586f405215&inputCurrency=0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA","_blank");'
    driver.execute_script(dackie_window)
    driver.switch_to.window(driver.window_handles[pre_index])
    connect_ele = wrapper_find_element(
        driver, '//div[@class="sc-3a5c8d1f-1 fQjBku"]')
    lazy_click(connect_ele)
    wallet_ele = wrapper_find_element(
        driver, '//div[contains(text(),"Metamask")]')
    lazy_click(wallet_ele)
    op.wallet_connect(pre_index)
    try:
        for number in range(1, 11):
            print(number)
            bot_swap(op)
    except Exception as err:
        print('bot swap error:', err)
    finally:
        op.wallet_disconnect(pre_index, 'www.dackieswap.xyz')
    op.wallet_lock(pre_index)
    op.wallet_quit()


bot_dackie()
