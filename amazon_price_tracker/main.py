import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os


SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
AMAZON_PRODUCT = "https://www.amazon.com/PETLIBRO-Automatic-Control-Stainless-Blockage/dp/B097KDM2NP/ref=sr_1_5?crid=2IFDZ1ZR206NI&dib=eyJ2IjoiMSJ9.eIJAzDAwoSUsN4KRXSmLK8fXzU6LIJWshtOfb4An42r8vDBFJ_Rfz4jScPnwZdfEeES5DRn6wX6wE64ZEdQPJX8CCp6T6QCZAJelXVwySuNWZVkTdGPL9vpzN4s-wXbsYZ2bqVuTteESItp0np15_ogAaBl9qIKbD_iwQ7t6aK4Mjn-bCdJB10z1AG9avOvj9uir3xk2KQI_2-7idEn7ng6P2AQ6vMd-nQeMOt3vPip6LA33jLBf-QQNU0avWsZJG_Is_hPMPQB3KaEprrRw8jzDbR8-DRILFbcSx1_bR3w.VnHAkauSEJlSd9cc4GJ56bXcQKjgsHw-3AVX-ssMXbE&dib_tag=se&keywords=dual%2Bautomatic%2Bcat%2Bfeeder&qid=1719226121&sprefix=dual%2Bautomati%2Caps%2C216&sr=8-5&th=1"
APP_PASSWORD = os.getenv("APP_PASSWORD")
SMTP_ADDR = os.getenv("SMTP_ADDR")


headers = {
    "Accept-Language": "en-US,en;q=0.9,en-GB;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

response = requests.get(AMAZON_PRODUCT, headers=headers)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price = soup.find(class_="a-offscreen").get_text()
price_no_currency = float(price.split("$")[1])
print(price_no_currency)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 95.00

if price_no_currency>BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP(SMTP_ADDR, port=587) as connection:
        connection.starttls()
        result = connection.login(SENDER_EMAIL, APP_PASSWORD)
        # connection.sendmail(
        #     from_addr=SENDER_EMAIL,
        #     to_addrs=RECEIVER_EMAIL,
        #     msg = f"Subject: Amazon Price Alert!\n\n{message}\n.{AMAZON_PRODUCT}".encode("utf-8")
        # )
        subject = "Amazon Price Alert!"
        body = f"\n\n{message}\n.{AMAZON_PRODUCT}"
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = "Python Bot <w818005@gmail.com>"
        msg["To"] = RECEIVER_EMAIL

        # Send the email
        connection.send_message(msg)