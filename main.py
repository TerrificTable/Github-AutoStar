from selenium.webdriver import ChromeOptions
from selenium import webdriver
from util.common import title
from util.login import login
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


def main():
    driver = webdriver.Chrome()
    if multiAcc == True:
        for user in usernames:
            url = "https://github.com/{}".format(user)
            login(driver, url)


if __name__ == "__main__":
    title("Idle")
    download_chromedriver()
    main()
