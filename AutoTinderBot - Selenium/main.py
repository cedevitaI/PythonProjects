from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://tinder.com/")

#decline cookies
try:
    decline_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='I accept']"))
    )
    decline_button.click()
except Exception as e:
    print("An error occurred: ", e)

sleep(2)
login_button = driver.find_element(By.XPATH, '//*[@id="q-612006581"]/div/div[1]/div/main/div[1]/div/div/div/div/div/header/div/div[2]/div[2]/a')
login_button.click()

#click the log in with google button

login_with_google = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Продолжете со Google']"))
)
login_with_google.click()

#switching to google login popup
main_window = driver.current_window_handle #store the current window handle

#waiting for new window
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
sleep(2)
#getting all window handles and switching to the new window
for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break

#enter email and password
sleep(3)
email_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@type="email"]'))
)
email_input.send_keys(EMAIL)
email_input.send_keys(Keys.RETURN)

sleep(3)
password_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))
)
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)


#switching back to main window after logging in
driver.switch_to.window(main_window)
sleep(5)
# if presented with a CAPTCHA - solve the puzzle manually
input("Press Enter when you have solved the Captcha")

#dismiss all the popups

location_popup = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="q1954579639"]/div/div/div/div/div[3]/button[1]/div[2]/div[2]'))
)
location_popup.click()

notification_popup = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="q1954579639"]/div/div/div/div/div[3]/button[2]/div[2]/div[2]/div'))
)
notification_popup.click()

for n in range(100):

    sleep(1) #so tinder doesn't think i'm a bot, 1 second delay between likes

    try:
        print("called")
        like_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'))
        )
        like_button.click()

    #Exception handling in case there is a match popup
    except ElementClickInterceptedException:
        try:
            match_popup = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(((By.CSS_SELECTOR, '.itsAMatch a')))
            )
            match_popup.click()

        except NoSuchElementException:
            sleep(2)


driver.quit()