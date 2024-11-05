# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# vim test.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd

counter=1
limit=37
options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://casosclinicosonline.spmi.pt/index.php")
div_element = driver.find_element(By.ID, "div_bt_next")
elements = driver.find_elements(By.CLASS_NAME, "fbox250.text14")

# List to store all hrefs
hrefs = []

# Iterate over each element and find <a> tags within them
for element in elements:
    anchor_tags = element.find_elements(By.TAG_NAME, "a")
    for anchor in anchor_tags:
        href = anchor.get_attribute("href")
        if href:  # Ensure the href is not None
            hrefs.append(href)

# Print all extracted hrefs
for href in hrefs:
    print(href)


df=list()

for href in hrefs:
    df.append({"source":href})


df=pd.DataFrame.from_dict(df)
df.to_csv("linksSPMI.csv")



driver.close()