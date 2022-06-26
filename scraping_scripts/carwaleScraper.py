import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

path = "/home/krish/Downloads/chromedriver"
url = "https://www.carwale.com/hyundai-cars/kona-electric/user-reviews"

#for headless-mode
options = Options()
options.headless = True

##############################################
"""
    To get all the links from Read More
"""
##############################################

links = []

for i in range(1, 5):
    website = url + "-p" + str(i) +"/"

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(website)

    lnks = driver.find_elements(by="xpath",
                                    value='//a[@class="o-eemiLE o-cYdrZi o-eqqVmt o-dCCCCt o-fzoTnS o-elzeOy o-dsALUH o-cpnuEd"]')

    for lnk in lnks:
        links.append(lnk.get_attribute("href"))


#print(links)


##############################################
"""
    To get data from the links
"""
##############################################


cols = ['review', 'Exterior', 'Comfort', 'Performance', 'Fuel Economy', 'Value for Money', 'Condition', 'driven']

df = pd.DataFrame(columns=cols)

for lnk in links:

    temp = {'review': 0, 'Exterior': 0, 'Comfort': 0, 'Performance': 0, 'Fuel Economy': 0, 'Value for Money': 0, 'Condition': 0, 'driven': 0, 'rating': 0}

    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(lnk)

    driver.implicitly_wait(2)
    review = driver.find_element(by="xpath", value='//div[@class="o-jjpuv o-fyWCgU o-eZTujG"]').text
    temp['review'] = [review]


    ratings = driver.find_elements(by="xpath", value='//div[@class="o-fcaNGp o-dsiSgT o-NBTwp o-dGBYL o-fzpihx o-fmBWBW o-daXxmY"]/div//*[name()="svg"][@class="IrB0ha RTjkn7 o-eNNlqh"]')

    temp['rating'] = len(ratings)

    attributes = driver.find_elements(by="xpath", value='//div[@class="o-fcaNGp o-dsiSgT o-NBTwp o-dGBYL "]')
    for attrib in attributes:
        attribs = attrib.text.split("\n")
        temp[attribs[1]] = [attribs[0]]

    others = driver.find_elements(by="xpath", value='//div[@class="o-eZTujG o-eigHmr"]')

    temp['Condition'] = [others[0].text]
    temp['driven'] = [others[1].text]

    driver.implicitly_wait(1)
    df = pd.concat([df, pd.DataFrame.from_dict(temp)], axis=0, ignore_index=True)
    print(df)
    break

# To save df
#df.to_csv("carwaleNexonNew.csv", mode='a', index=False, header=None)

driver.quit()


