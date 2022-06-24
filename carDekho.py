import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re

path = "/home/krish/Downloads/chromedriver"

website = "https://www.cardekho.com/tata/nexon-ev/user-reviews"

attribs = ['mileage', 'performance', 'looks', 'comfort', 'engine', 'interior', 'power', 'price', 'safety', 'service', 'ac', 'maintenance', 'safety', 'speed', 'seat', 'space', 'style', 'clearance', 'dealer', 'experience', 'ground', 'maintenance', 'noise', 'pickup', 'service', 'torque', 'driver', 'headlamp', 'infotainment', 'rear', 'seat', 'steering', 'sunroof', 'suv', 'warranty', 'airbags', 'alloy', 'automatic', 'cabin', 'cabin', 'comparison', 'exterior', 'gear', 'legroom', 'lights', 'music', 'music', 'parking', 'parts', 'sensors', 'service', 'service', 'showroom', 'touch', 'vent', 'wheel']

for attribute in attribs:
    try:
        website = "https://www.cardekho.com/tata/nexon-ev/user-reviews"
        website = website + "/" + attribute

        service = Service(executable_path=path)
        driver = webdriver.Chrome(service=service)
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
                    if rev.text:
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

        df.to_csv("reviews/Newcardekho.csv", mode='a', index=False, header=None)

        print(df)

        driver.quit()

    except:
        pass


#for container in containers:
    #attributes = container.find_elements(by="xpath", value="./li[@class=' shadow24']")
    #for attribute in attributes:
        #text = attribute.text
        #attribs.append(re.findall(r"(?i)\b[a-z]+\b", text.lower())[0])


#for category in categories:
    #attributes = category.find_elements(by="xpath", value="./li[@class=' shadow24']")
    #for attribute in attributes:
        #text = attribute.text
        #attribs.append(re.findall(r"(?i)\b[a-z]+\b", text.lower())[0])
