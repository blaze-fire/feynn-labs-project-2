import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re

path = "/home/krish/Downloads/chromedriver"

GlobalWebsite = "https://www.cardekho.com/mg/zs-ev/user-reviews"


#for headless-mode
options = Options()
options.headless = True

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(GlobalWebsite)

containers = driver.find_elements(by="xpath",
                                value='//ul[@class="galleryNav ReviewsTab marginBottom20"]')

driver.find_element(by="xpath",
                    value="//ul[@class='galleryNav ReviewsTab marginBottom20']/li[@id='moretab']").click()

driver.implicitly_wait(2) # seconds

categories = driver.find_elements(by="xpath",
                                value="//div[@class='recommendedCars']/ul[@class='galleryNav ReviewsTab marginBottom20']")
attribs = []

for container in containers:
    attributes = container.find_elements(by="xpath", value="./li[@class=' shadow24']")
    for attribute in attributes:
        text = attribute.text
        attribs.append(re.findall(r"(?i)\b[a-z]+\b", text.lower())[0])


for category in categories:
    attributes = category.find_elements(by="xpath", value="./li[@class=' shadow24']")
    for attribute in attributes:
        text = attribute.text
        attribs.append(re.findall(r"(?i)\b[a-z]+\b", text.lower())[0])


print(attribs)


for attribute in attribs:
    try:
        website = GlobalWebsite
        website = website + "/" + attribute

        service = Service(executable_path=path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(website)

        containers = driver.find_elements(by="xpath",
                                        value='//ul[@class="galleryNav ReviewsTab marginBottom20"]')

        driver.find_element(by="xpath",
                            value="//ul[@class='galleryNav ReviewsTab marginBottom20']/li[@id='moretab']").click()

        driver.implicitly_wait(2) # seconds

        categories = driver.find_elements(by="xpath",
                                        value="//div[@class='recommendedCars']/ul[@class='galleryNav ReviewsTab marginBottom20']")

        stars = driver.find_elements(by="xpath", value="//div[@class='readReviewBox']")

        df = pd.DataFrame(columns=["review", "rating", "attribute"])

        for star in stars:

            try:
                review = star.find_elements(by="xpath", value="./div/div[@class='contentspace']/p/span")
                for rev in review:

                    if rev.text == "Read More":
                        pass

                    elif rev.text:
                        review = rev.text

            except:
                pass

            rating = 0
            for i in range(1, 6):
                try:
                    if star.find_elements(by="xpath", value=f"./div/div/div/span/span[@class='stars stars{i} icon-star-full-fill ']"):
                        rating = max(rating, i)

                    elif star.find_elements(by="xpath", value=f"./div/div/div/span/span[@class='stars stars{i} icon-star-half-empty ']"):
                        rating += 0.5
                except:
                    pass

            df = pd.concat([df, pd.DataFrame({"review": [review], "rating": [rating], "attribute": [attribute]})], axis=0, ignore_index=True)

        print(df)
        # df.to_csv("reviews/Newcardekho.csv", mode='a', index=False, header=None)
        driver.quit()

    except:
        pass



