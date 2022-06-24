import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

path = "/home/krish/Downloads/chromedriver"

for i in range(1, 2):

    website = "https://www.bikewale.com/techoelectra-bikes/raptor/reviews/page/" + str(i) + "/"

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)

    containers = driver.find_elements(by="xpath",
                                      value='//li[@class="list-item"]')

    reviews = []

    for container in containers:
        values = container.find_elements(by="xpath", value=".//div[@class='main-content']")

        for value in values:
            reviews.append(value.text)

    attributes = []
    ratings = []

    for container in containers:
        attribute = []
        attribs = container.find_elements(by="xpath", value="./div/ul/li/div/p[@class='font14 text-slate-grey']")
        for rev in attribs:
            attribute.append(rev.text)

        attributes.append(attribute)

        rating = container.find_element(by="xpath", value="./div/div/span[@class='rating-badge']")
        ratings.append(rating.text)

    review_dict = {"reviews": reviews, "attributes": attributes, "ratings": ratings}

    df = pd.DataFrame.from_dict(review_dict)
    df.to_csv("reviews/e2w.csv", mode='a', index=False, header=None)

    print("len of reviews {}, len of attribs {}".format(len(reviews), len(attributes)))
    driver.quit()



# //li[@class="list-item"]/div/div/span[@class="rating-badge"]
