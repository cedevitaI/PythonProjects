from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options = chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

#finding the cookie
cookie = driver.find_element(by = By.ID, value = "cookie")

#finding the items
items = driver.find_elements(by = By.CSS_SELECTOR, value = "#store div")
items_id = [item.get_attribute("id") for item in items]

timeout = time.time()+5
five_minutes = time.time() + 60*5

while True:
    cookie.click()

    if time.time() > timeout:
        all_prices = driver.find_elements(by = By.CSS_SELECTOR, value = "#store b")
        items_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                items_prices.append(cost)

        #dictionary of items and their prices
        cookies_upgrade = {}
        for n in range(len(items_prices)):
            cookies_upgrade[items_prices[n]] = items_id[n]

        #current cookie count
        money_element = driver.find_element(by = By.ID, value = "money").text
        if "," in money_element:
            money_element = money_element.replace(",","")
        cookie_count = int(money_element)

        #find affordable upgrades
        affordable_upgrades = {}
        for cost, id in cookies_upgrade.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        #purchase highest price item
        highest_price_affordable_item = max(affordable_upgrades)
        print(highest_price_affordable_item)
        to_purchase_id = affordable_upgrades[highest_price_affordable_item]

        driver.find_element(by = By.ID, value = to_purchase_id).click()

        timeout = time.time()+5

    if time.time() > five_minutes:
        cookies_per_s = driver.find_element(by = By.ID, value = "cps").text
        print(cookies_per_s)
        break

