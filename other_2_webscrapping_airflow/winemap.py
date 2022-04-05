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

def web_scrapping(current_date,Webpage,Country,Region):

    Show_menu = driver.find_element(By.CSS_SELECTOR, '.select-filter-show')
    Show_menu.click()
    onehun_button = Show_menu.find_elements(By.TAG_NAME, 'option')[-1]
    onehun_button.click()
    time.sleep(3)
    Product_menu = driver.find_element(By.CSS_SELECTOR, '.col-sm-9')
    for products in Product_menu.find_elements(By.CSS_SELECTOR, '.product-grid'):
        Product_caption = products.find_element(By.CSS_SELECTOR, '.product-title')
        Product_caption_text = Product_caption.find_element(By.TAG_NAME, 'a').text
        if "," not in Product_caption_text:
            continue
        Product_list = Product_caption_text.split(",")
        sub_list_01 = Product_list[0].split(" ")
        sub_list_02 = Product_list[1].split(" ")
        temp_01_list = []
        for elements_01 in sub_list_01:
            if elements_01.isdigit():
                Year = elements_01
            else:
                temp_01_list.append(elements_01)
        Garden = (" ").join(temp_01_list)
        for elements_02 in sub_list_02:
            if elements_02 == "750ml":
                temp_02 = sub_list_02.index(elements_02)
                Sub_division = ((" ").join(sub_list_02[0:temp_02])).strip(' ')
        if Sub_division == '':
            Sub_division = "no data"
        Price = products.find_element(By.CSS_SELECTOR, '.price').text.replace('$','').replace('.00','').replace('"','').replace(',','')
        all_products.append([current_date, Webpage, Country, Region, Sub_division, Year, Garden, Price])


#######################################################################################

today = datetime.today()
current_date = today.strftime('%Y-%m-%d')
Country = 'France'
Webpage = 'Winemap'


chrome_options = Options()
chrome_options.add_argument("--headless")

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=chrome_options,service=s)

driver.get("https://www.winemap.hk/index.php?route=product/category&path=20_27")

Show_menu = driver.find_element(By.CSS_SELECTOR, '.select-filter-show')
onehun_button = Show_menu.find_elements(By.TAG_NAME, 'option')[-1]
onehun_button.click()
all_products = []
Region_menu = driver.find_element(By.CSS_SELECTOR, '.cat-name')
Region_menu_len = len(Region_menu.find_elements(By.TAG_NAME, 'a'))
for i in range(Region_menu_len):
    Region_menu = driver.find_element(By.CSS_SELECTOR, '.cat-name')
    Region_button = Region_menu.find_elements(By.TAG_NAME, 'a')[i]
    Region = Region_button.text
    print(Region)
    Region_button.click()
    #######################################################################################
    time.sleep(3)
    web_scrapping(current_date, Webpage, Country, Region)
    time.sleep(3)
    #######################################################################################
    back_menu = driver.find_element(By.CSS_SELECTOR, '.breadcrumb')
    back_button = back_menu.find_elements(By.TAG_NAME, 'li')[2]
    back_button.click()

# print(all_products)

driver.close()

Redwine = pd.DataFrame(all_products, columns=['Date','Webpage','Country','Region','Subdivision','Year','Garden','Price'])
Redwine.to_csv(f'Redwine_winemap_{current_date}.csv',index=False)

os.environ.setdefault("GCLOUD_PROJECT", "divine-builder-342012")
storage_client = storage.Client.from_service_account_json("divine-builder-342012-282613dd5939.json")
bucket = storage_client.get_bucket('bucket-redwine')
blob = bucket.blob(f'Redwine_winemap_{current_date}.csv')
blob.upload_from_filename(f'./Redwine_winemap_{current_date}.csv')


config = {
    'user': 'root',
    'password': 'joniwhfe',
    'host': '34.92.69.178',
    'database' : 'Redwine_testing'
}

hadoop_redwine = mysql.connector.connect(**config)
cursor = hadoop_redwine.cursor()
#


df = pd.read_csv(f"Redwine_winemap_{current_date}.csv")
df = df.astype({col: 'string' for col in df.select_dtypes('int64').columns})
query = (
        "INSERT INTO Redwine_testing (Date,Webpage,Country,Region,Subdivision,Year,Garden,Price) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

cursor.executemany(query, list(df.to_records(index=False)))
hadoop_redwine.commit()


