import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

path = "/home/krish/Downloads/chromedriver"

for i in range(1, 6):
    website = "https://www.team-bhp.com/forum/electric-cars/230585-hyundai-kona-ev-ownership-review"
    website = website + '-' + str(i) + ".html"

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)

    containers = driver.find_elements(by="xpath",
                                      value='//td[@class="alt1"]/div')

    reviews = []

    for container in containers:
        review = container.text
        reviews.append(review)

    print(reviews)

    review_dict = {"reviews": reviews}

    df = pd.DataFrame.from_dict(review_dict)
    df.to_csv("reviews/hyundaiKonaTeamBHP.csv", mode='a', index=False, header=None)
    driver.quit()

