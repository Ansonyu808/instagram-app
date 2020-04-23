import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
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

            self.username = self.get_user_input('username')
            username.send_keys(self.username)
            password.send_keys(self.get_user_input('password'))

            login_xpath = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div'
            self.driver.find_element_by_xpath(login_xpath).click()

            notifications_xpath = '/html/body/div[4]/div/div/div[3]/button[2]'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, notifications_xpath))).click()
        except:
            raise

    def get(self, type):
        xpath_num = 0
        if type == 'following':
            xpath_num = 3
        elif type == 'followers':
            xpath_num = 2
        else:
            return

        self.navigate_to_profile_page()

        follow_button_xpath = f'/html/body/div[1]/section/main/div/header/section/ul/li[{xpath_num}]/a'
        follow_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, follow_button_xpath)))
        num_follow = int(self.driver.find_element_by_xpath(
            f'/html/body/div[1]/section/main/div/header/section/ul/li[{xpath_num}]/a/span').text)
        follow_button.click()
        sleep(2)

        scroll_popup = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        self.scroll_to_bottom(scroll_popup)

        bucket = {
            'following': self.following,
            'followers': self.followers
        }
        for i in range(1, num_follow + 1):
            xpath = f'/html/body/div[4]/div/div[2]/ul/div/li[{i}]/div/div[1]/div[2]/div[1]/a'
            try:
                name = self.driver.find_element_by_xpath(xpath).text
                bucket[type].add(name)
            except Exception as e:
                print(e)

    def scroll_to_bottom(self, element):
        last_ht, ht = 0, 1
        while ht > last_ht:
            last_ht = ht
            ht = self.driver.execute_script('''
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
            ''', element)
            sleep(1.5)

    def navigate_to_profile_page(self):
        self.driver.get(f'https://www.instagram.com/{self.username}/')

    def get_user_input(self, input_type):
        return input(f'Please enter {input_type}\n')


test = InstagramWebDriver()
test.login()
test.get('followers')
test.get('following')
print(test.following)
print(test.followers)
print(test.following - test.followers)
print(test.followers - test.following)
