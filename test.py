from selenium.webdriver import ChromeOptions
from selenium import webdriver
from util.common import debug
from time import sleep
from lxml import html
import json


headless = False
options = ChromeOptions()
options.headless = headless
options.add_experimental_option("excludeSwitches", ["enable-logging"])

stared = []
driver = webdriver.Chrome(options=options)
url = "https://github.com/TerrificTable"
driver.get(url)


driver.find_element_by_xpath(
    '//*[@id="js-pjax-container"]/div[1]/div/div/div[2]/div/nav/a[2]').click()
sleep(1)
tree = html.fromstring(driver.page_source)


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


def loaded(xpath, xpath1=None):
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


get_config()
for product_tree in tree.xpath('//*[@id="user-repositories-list"]/ul'):
    titles = product_tree.xpath('//a[@itemprop="name codeRepository"]/text()')
    for title in titles:
        title = str(title).replace(" ", "").replace("\n", "")
        driver.get(url + f"/{title}")

        star = loaded('//button[contains(@data-ga-click, "text:Star")]',
                      '//a[@aria-label="You must be signed in to star a repository"]')
        star.click()

        username = driver.find_element_by_xpath('//*[@id="login_field"]')
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
            debug.error("Invalid Logins")
            input()
            exit()
        except:
            stared.append(title)
            debug.working("Stared {}".format(title))
            
        sleep(2)
