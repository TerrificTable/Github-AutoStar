from selenium.webdriver import ChromeOptions
from selenium import webdriver
from util.common import title
from time import sleep
from lxml import html
import requests
import zipfile
import json
import wget
import os


headless = False
options = ChromeOptions()
options.headless = headless
options.add_experimental_option("excludeSwitches", ["enable-logging"])


def get_config():
    global username, usernames, multiAcc
    with open("./config.json") as f:
        config = json.load(f)

        multiAcc = config["Multible-Accounts"]
        if str(multiAcc) == "true":
            multiAcc = True
            usernames = config["Github-Usernames"]
        username = config["Github-Username"]


def download_chromedriver():
    if not os.path.isfile(f"{os.getcwd()}/chromedriver.exe"):
        url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        response = requests.get(url)
        version_number = response.text

        download_url = "https://chromedriver.storage.googleapis.com/" + \
            version_number + "/chromedriver_win32.zip"

        latest_driver_zip = wget.download(download_url, 'chromedriver.zip')

        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall()
            print("Chromedriver Installed")
        os.remove(latest_driver_zip)


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


def main():
    driver = webdriver.Chrome()
    if multiAcc == True:
        for user in usernames:
            url = "https://github.com/{}".format(user)
            driver.get(url)
            driver.find_element_by_xpath(
                '//*[@id="js-pjax-container"]/div[1]/div/div/div[2]/div/nav/a[2]').click()
            tree = html.fromstring(driver.page_source)

            for product_tree in tree.xpath('//*[@id="user-repositories-list"]/ul'):
                titles = product_tree.xpath(
                    '//a[@itemprop="name codeRepository"]/text()')
                for title in titles:
                    title = str(title).replace(" ", "").replace("\n", "")
                    print(title)
                    driver.get(url + f"/{title}")

                    star = loaded(driver,
                                  '//button[contains(@data-ga-click, "text:Star")]',
                                  '//a[@aria-label="You must be signed in to star a repository"]')
                    star.click()


if __name__ == "__main__":
    title("Idle")
    download_chromedriver()
    main()
