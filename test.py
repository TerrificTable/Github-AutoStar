from selenium.webdriver import ChromeOptions
from selenium import webdriver
from time import sleep
from lxml import html


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


for product_tree in tree.xpath('//*[@id="user-repositories-list"]/ul'):
    titles = product_tree.xpath('//a[@itemprop="name codeRepository"]/text()')
    for title in titles:
        title = str(title).replace(" ", "").replace("\n", "")
        print(title)
        driver.get(url + f"/{title}")

        star = loaded('//button[contains(@data-ga-click, "text:Star")]',
                      '//a[@aria-label="You must be signed in to star a repository"]')
        star.click()