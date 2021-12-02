from util.common import debug
from time import sleep
from lxml import html


stared = []


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


def login(driver, usernames, multiAcc, logins: list):
    if multiAcc:
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

                    username = driver.find_element_by_xpath(
                        '//*[@id="login_field"]')
                    password = driver.find_element_by_xpath(
                        '//*[@id="password"]')

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
                        debug.error("Invalid Logins\n")
                        input()
                        exit()
                    except:
                        debug.working("Stared {}\n".format(title))
                    sleep(2)
    else:
        user = usernames[0]
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

                username = driver.find_element_by_xpath(
                    '//*[@id="login_field"]')
                password = driver.find_element_by_xpath(
                    '//*[@id="password"]')

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
                    debug.error("Invalid Logins\n")
                    input()
                    exit()
                except:
                    debug.working("Stared {}\n".format(title))
                sleep(2)
