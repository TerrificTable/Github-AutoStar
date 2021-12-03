import os
from colorama import Fore
import random
import shutil
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from util.common import debug
from time import sleep
from lxml import html
import json


stared = []


def get_config():
    global usernames, multiAcc, logins
    with open("./config.json") as f:
        config = json.load(f)

        multiAcc = config["Multible-Accounts"]
        if str(multiAcc) == "true":
            multiAcc = True
            usernames = config["Github-Usernames"]
        username = config["Github-Username"]
        logins = config["logins"]


def loaded(driver, xpath, xpath1=None):
    try:
        elm = driver.find_element_by_xpath(xpath)
        return elm
    except Exception as e:
        try:
            if xpath1 != None:
                elm = driver.find_element_by_xpath(xpath1)
                return elm
        except:
            pass
        sleep(1)
        loaded(xpath)


amt = 0


def mfa(driver):
    global amt
    try:
        mfaInput = driver.find_element_by_xpath('//*[@id="otp"]')
        mfaCode = input("2FA Code: ")
        mfaInput.clear()
        mfaInput.send_keys(mfaCode)
    except:
        amt += 1
        if amt > 1:
            pass
        sleep(1)
        mfa(driver)


def main(headless):
    get_config()
    options = ChromeOptions()
    options.headless = headless
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    url = "https://github.com/TerrificTable"
    driver.get(url)

    driver.find_element_by_xpath(
        '//*[@id="js-pjax-container"]/div[1]/div/div/div[2]/div/nav/a[2]').click()
    sleep(1)
    tree = html.fromstring(driver.page_source)
    for product_tree in tree.xpath('//*[@id="user-repositories-list"]/ul'):
        titles = product_tree.xpath(
            '//a[@itemprop="name codeRepository"]/text()')
        for title in titles:
            title = str(title).replace(" ", "").replace("\n", "")
            driver.get(url + f"/{title}")

            star = loaded(driver,
                          '//button[contains(@data-ga-click, "text:Star")]',
                          '//a[@aria-label="You must be signed in to star a repository"]')
            star.click()

            username = driver.find_element_by_xpath(
                '//*[@id="login_field"]')
            password = driver.find_element_by_xpath('//*[@id="password"]')

            username.clear()
            username.send_keys(logins[0])

            password.clear()
            password.send_keys(logins[1])

            driver.find_element_by_xpath(
                '//*[@id="login"]/div[4]/form/div/input[12]').click()
            sleep(1)
            try:
                driver.find_element_by_xpath(
                    '//*[@id="js-flash-container"]/div/div')
                debug.error(" Invalid Logins")
                input()
            except:
                mfa(driver)
                stared.append(title)
                debug.working(" Stared {}".format(title))
            sleep(2)


def ui():
    os.system("cls;clear")
    columns = shutil.get_terminal_size().columns
    print(f"{Fore.CYAN} ██████╗ ██╗████████╗███████╗████████╗ █████╗ ██████╗ {Fore.WHITE}".center(columns))
    print(f"{Fore.CYAN}██╔════╝ ██║╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗{Fore.WHITE}".center(columns))
    print(f"{Fore.CYAN}██║  ███╗██║   ██║   ███████╗   ██║   ███████║██████╔╝{Fore.WHITE}".center(columns))
    print(f"{Fore.CYAN}██║   ██║██║   ██║   ╚════██║   ██║   ██╔══██║██╔══██╗{Fore.WHITE}".center(columns))
    print(f"{Fore.CYAN}╚██████╔╝██║   ██║   ███████║   ██║   ██║  ██║██║  ██║{Fore.WHITE}".center(columns))
    print(f"{Fore.CYAN} ╚═════╝ ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝{Fore.WHITE}".center(columns))
    print(
        f"Made by: {Fore.MAGENTA}TerrificTable55™#5297{Fore.WHITE}".center(columns))
    print("\n\n")
    headless = input(
        f"\t\t\t\t     {Fore.WHITE}[{Fore.MAGENTA}>{Fore.WHITE}] Run Headless [y/n]: ")  # .center(columns)
    input(f"Press {Fore.YELLOW}ENTER{Fore.WHITE} to start".center(columns))
    main(headless)


ui()
