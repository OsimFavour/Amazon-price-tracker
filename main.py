from requests_html import HTMLSession
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

BUY_PRICE = 200
URL = "https://www.amazon.com/Dell-Latitude-E5450-Certified-Refurbished/dp/B07CTRFHW9"


class AmazonTracker:
    
    def __init__(self) -> None:
        self.session = HTMLSession()
        r = self.session.get(URL)
        r.html.render(sleep=1, timeout=20)
        self.product = {
            "title": r.html.xpath('//*[@id="productTitle"]', first=True).text,
            "price": r.html.xpath('//*[@id="corePrice_feature_div"]/div/span/span[2]', first=True).text
            }
        self.price_alert = 'Subject: Instant Laptop Price Alert:'
        self.message = f"{self.product['title']} is now {self.product['price']} below your target price, Buy now!"

        print(self.product)

    def product_condition(self, price):
        price = float(self.product["price"].replace("$", ""))
        if price < BUY_PRICE:
            return price

    def send_email(self):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"{self.price_alert}\n\n{self.message}\n\n{URL}"
            )


laptop_price = AmazonTracker()
emails = laptop_price.send_email()
laptop_price.product_condition(emails)






