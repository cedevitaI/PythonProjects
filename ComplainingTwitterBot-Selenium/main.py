from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep



TWITTER_EMAIL = os.getenv("twitter_email")
TWITTER_PW = os.getenv("twitter_password")
PROMISED_DOWN = 100
PROMISED_UP = 50

class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        sleep(2)

        go_button = self.driver.find_element(By.XPATH, '//span[text() = "Go"]')
        go_button.click()

        sleep(50)

        self.down = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span'))
        ).text

        self.up = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span'))
        ).text

        print("Down: ", self.down)
        print("Up: ", self.up)

    def tweet_at_provider(self):
        self.driver.get("https://x.com/login")
        sleep(2)

        try:
            # switch to iframe if required
            iframe = self.driver.find_element(By.XPATH, "//iframe[contains(@src, 'google.com')]")
            self.driver.switch_to.frame(iframe)

            # try to locate the login button
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Sign in with Google")]'))
            )
            login_button.click()

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            self.driver.switch_to.default_content()

        sleep(5)

        #finding the google login popup
        main_window = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if handle != main_window:
                self.driver.switch_to.window(handle)
                break

        sleep(3)
        email_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="email"]'))
        )
        email_input.send_keys(TWITTER_EMAIL)
        email_input.send_keys(Keys.RETURN)

        sleep(3)
        password_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))
        )
        password_input.send_keys(TWITTER_PW)
        password_input.send_keys(Keys.RETURN)

        input("Press enter after doing google auth")

        # switching bad to main window after logging in
        self.driver.switch_to.window(main_window)
        sleep(5)

        tweet_compose = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="textbox"][aria-label="Post text"]'))
        )
        complaint = (f'#MakedonskiTelekom, зошто е брзината на мојот интернет {self.down}down/{self.up}up, '
                     f'кога плаќам за 300down/300up?')
        tweet_compose.send_keys(complaint)
        sleep(5)

        tweet_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div'
                                                          '/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]'
                                                          '/div[2]/div/div/div/button/div/span/span')
        tweet_button.click()
        # self.driver.quit()



driver = InternetSpeedTwitterBot()
driver.get_internet_speed()
driver.tweet_at_provider()







