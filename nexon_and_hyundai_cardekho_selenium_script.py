import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

path = "/home/krish/Downloads/chromedriver"

for i in range(2, 4):
    website = "https://www.cardekho.com/hyundai/kona/user-reviews"
    website = website + '/' + str(i)
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)

    containers = driver.find_elements(by="xpath",
                                      value='//div[@class="contentspace"]')

    reviews = []

    for container in containers:
        review = container.find_element(by="xpath", value='./p/span').text

        reviews.append(review)

    print(reviews)

    review_dict = {"reviews": reviews}

    df = pd.DataFrame.from_dict(review_dict)
    df.to_csv("hyundai_kona_reviews.csv", mode='a', index=False, header=None)
    driver.quit()
