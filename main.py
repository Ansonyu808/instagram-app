import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramWebDriver:
    def __init__(self):
        self.chrome_driver_path = os.getcwd() + '\\chromedriver.exe'
        self.username = ''
        self.followers = set()
        self.following = set()

        self.driver = webdriver.Chrome(self.chrome_driver_path)
        self.driver.get("http://instagram.com")

        self.wait = WebDriverWait(self.driver, 5)

    def login(self):
        try:
            username = self.wait.until(EC.element_to_be_clickable((By.NAME, 'username')))
            password = self.wait.until(EC.element_to_be_clickable((By.NAME, 'password')))

            self.username = 'ansonyu808'
            username.send_keys(self.username)
            password.send_keys('Easyas123')
            # self.username = self.get_user_input('username')
            # username.send_keys(self.username)
            # password.send_keys(self.get_user_input('password'))

            # Click login button
            login_xpath = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div'
            self.driver.find_element_by_xpath(login_xpath).click()

            # If notifications appears, click  "Not Now "
            notifications_xpath = '/html/body/div[4]/div/div/div[3]/button[2]'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, notifications_xpath))).click()
        except:
            raise

    def get_followers(self):
        self.navigate_to_profile_page()

        followers_button_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'
        self.wait.until(EC.element_to_be_clickable((By.XPATH, followers_button_xpath))).click()
        sleep(2)

        scroll_popup = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        self.scroll_to_bottom(scroll_popup)
        print("Finished Scrolling")

        links = scroll_popup.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.followers = names

    def scroll_to_bottom(self, element):
        last_ht, ht = 0, 1
        while ht > last_ht:
            last_ht = ht
            ht = self.driver.execute_script('''
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
            ''', element)
            sleep(1)

    def navigate_to_profile_page(self):
        self.driver.get(f'https://www.instagram.com/{self.username}/')

    def get_user_input(self, input_type):
        return input(f'Please enter {input_type}\n')


test = InstagramWebDriver()
test.login()
test.get_followers()

