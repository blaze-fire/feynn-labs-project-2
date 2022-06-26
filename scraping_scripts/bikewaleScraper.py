import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

path = "/home/krish/Downloads/chromedriver"
url = "https://www.bikewale.com/gemopai-bikes/ryder/reviews/"

#for headless-mode
options = Options()
options.headless = True

##############################################
"""
    To get all the links
"""
##############################################

links = []

for i in range(1, 2):
    website = url + "page/" + str(i) +"/"

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(website)

    lnks = driver.find_elements(by="xpath",
                                    value='//a[@class="list-item-title inline-block margin-right5"]')

    for lnk in lnks:
        links.append(lnk.get_attribute("href"))

print(links)




##############################################
"""
    To get data from the links
"""
##############################################


cols = ['review', 'Used it for', 'Owned for', 'Ridden for', 'rating']

df = pd.DataFrame(columns=cols)

index = 0

for lnk in links:

    lnk = lnk.replace('\n', '')
    service = Service(executable_path=path)

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(lnk)

    driver.implicitly_wait(2)

    review = driver.find_element(by="xpath", value='//div[@class="font14 text-slate-grey"]/p').text
    df.loc[index, 'review'] = review

    attributes = driver.find_elements(by="xpath", value='//ul[@class="rating-circle-list"]')

    for attrib in attributes:
        attribs = attrib.text.split("\n")

        for i in range(1, len(attribs), 2):
            column = attribs[i]
            df.loc[index, column] = attribs[i-1]

    others = driver.find_elements(by="xpath", value='//div[@class="grid-3 omega padding-left20"]//p[@class="font14 text-slate-grey"]')

    rating = driver.find_element(by="xpath", value='//span[@class="rating-badge"]').text

    df.loc[index, 'rating'] = rating

    try:
        df.loc[index, 'Used it for'] = others[0].text
    except:
        pass

    try:
        df.loc[index, 'Owned for'] = others[1].text
    except:
        pass

    try:
        df.loc[index, 'Ridden for'] = others[2].text
    except:
        pass

    driver.implicitly_wait(1)
    #print(df)
    index += 1

df.to_csv("bikewaleNew.csv", mode='a', index=False)

driver.quit()


