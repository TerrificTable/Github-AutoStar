from selenium.webdriver import ChromeOptions
from selenium import webdriver
from util.common import title
from util.login import login
import requests
import zipfile
import json
import wget
import os


headless = False
options = ChromeOptions()
options.headless = headless
options.add_experimental_option("excludeSwitches", ["enable-logging"])
usernames = []


def get_config():
    with open("./config.json") as f:
        config = json.load(f)

        multiAcc = config["Multible-Accounts"]
        if str(multiAcc) == "true":
            multiAcc = True
            usernames = config["Github-Usernames"]
        else:
            usernames = []
        username = config["Github-Username"]
        logins = config['logins']
        return usernames, username, multiAcc, logins


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
        os.remove(latest_driver_zip)


def main():
    driver = webdriver.Chrome(options=options)
    if not multiAcc:
        usernames = [].append(username)
    login(driver, usernames, multiAcc, logins)


if __name__ == "__main__":
    title("Installing Chromedriver")
    download_chromedriver()
    title("Starting")
    usernames, username, multiAcc, logins = get_config()
    main()


# make UI
