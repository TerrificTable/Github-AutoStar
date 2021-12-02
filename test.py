from selenium.webdriver import ChromeOptions
from selenium import webdriver
from time import sleep
from lxml import html
import json


headless = False
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


def get_config():
    global username, usernames, multiAcc, login_username, login_password
    with open("./config.json") as f:
        config = json.load(f)

        multiAcc = config["Multible-Accounts"]
        if str(multiAcc) == "true":
            multiAcc = True
            usernames = config["Github-Usernames"]
        username = config["Github-Username"]
        login_username = config["logins"]["username"]
        login_password = config["logins"]["password"]


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
        print(title)
        driver.get(url + f"/{title}")

        star = loaded('//button[contains(@data-ga-click, "text:Star")]',
                      '//a[@aria-label="You must be signed in to star a repository"]')
        star.click()

        username = driver.find_element_by_xpath('//*[@id="login_field"]')
        password = driver.find_element_by_xpath('//*[@id="password"]')

        username.clear()
        username.send_keys(login_username)

        password.clear()
        password.send_keys(login_password)

        driver.find_element_by_xpath(
            '//*[@id="login"]/div[4]/form/div/input[12]').click()
        sleep(1)
        try:
            driver.find_element_by_xpath(
                '//*[@id="js-flash-container"]/div/div')
            sleep(1000000)
        except:
            pass
        sleep(2)

# "username": "YOUR USERNAME/EMAIL FOR GITHUB",
# "password": "YOUR GITHUB PASSWORD (needed for login to star repo)"
