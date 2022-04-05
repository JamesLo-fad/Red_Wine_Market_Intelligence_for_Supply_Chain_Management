from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import re
import time
import pandas as pd
import mysql.connector
from gcloud import storage
import os
########################################################################################






#######################################################################################





today = datetime.today()
current_date = today.strftime('%Y-%m-%d')
Country = 'France'
Webpage = 'Winecouple'

all_products = []

chrome_options = Options()
chrome_options.add_argument("--headless")

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=chrome_options,service=s)
webpage_list = ["bordeaux",'burgundy','rhone']
for w in range(3):
    webpage = webpage_list[w]
    driver.get(f"https://www.winecouple.hk/categories/{webpage}")
    Show_menu = driver.find_element(By.CSS_SELECTOR, '.js-select-limit')
    Show_menu.click()
    Show_seventwo = Show_menu.find_elements(By.TAG_NAME, 'li')[2]
    Show_seventwo.click()
    Product_menu = driver.find_element(By.CSS_SELECTOR, '.ProductList-list')
    for elements in Product_menu.find_elements(By.CSS_SELECTOR, '.info-box-inner-wrapper'):
        empty_list = []

        webpage = webpage.capitalize()
        if "," not in elements.text:
            product_caption  =  elements.find_element(By.CSS_SELECTOR, '.text-primary-color')
            price = elements.find_element(By.CSS_SELECTOR, '.price').text.replace('$','').replace('.00','').replace('HK','')
            if '~' in price:
                price = price.split("~")[1]
            product_text = product_caption.text
            product_list = product_text.split(" ")
            for stuff_01 in product_list:
                if stuff_01.isdigit():
                    temp = product_list.index(stuff_01)
                    Garden = " ".join(product_list[0:temp])
                    Garden = re.sub("[^A-Za-z]", " ", Garden.strip()).strip('    ')
                    Year = product_list[temp]
                    list_subdivision = product_list[temp+1:]
                    for x in list_subdivision:
                        if re.findall("^[a-zA-Z]*$",x):
                            empty_list.append(x)
                    Subdivision = " ".join(empty_list)
                    if Subdivision == "":
                        Subdivision = 'no data'
                    all_products.append([current_date, Webpage, Country, webpage, Subdivision, Year, Garden, price])
                    break

Redwine = pd.DataFrame(all_products, columns=['Date','Webpage','Country','Region','Sub-division','Year','Garden','Price'])
Redwine.to_csv(f'Redwine_winecouple_{current_date}.csv',index=False)


os.environ.setdefault("GCLOUD_PROJECT", "divine-builder-342012")
storage_client = storage.Client.from_service_account_json("divine-builder-342012-282613dd5939.json")
bucket = storage_client.get_bucket('bucket-redwine')
blob = bucket.blob(f'Redwine_winecouple_{current_date}.csv')
blob.upload_from_filename(f'./Redwine_winecouple_{current_date}.csv')


config = {
    'user': 'root',
    'password': 'joniwhfe',
    'host': '34.92.69.178',
    'database' : 'Redwine_testing'
}

hadoop_redwine = mysql.connector.connect(**config)
cursor = hadoop_redwine.cursor()


df = pd.read_csv(f"Redwine_winecouple_{current_date}.csv")
df = df.astype({col: 'string' for col in df.select_dtypes('int64').columns})
query = (
        "INSERT INTO Redwine_testing (Date,Webpage,Country,Region,Subdivision,Year,Garden,Price) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

cursor.executemany(query, list(df.to_records(index=False)))
hadoop_redwine.commit()