import mysql.connector
import pandas as pd

config = {
    'user': 'root',
    'password': 'joniwhfe',
    'host': '34.92.69.178',
    'database' : 'Redwine_testing'
}

hadoop_redwine = mysql.connector.connect(**config)
cursor = hadoop_redwine.cursor()

cursor.execute("CREATE TABLE Redwine_testing ("
               "Date VARCHAR(255),"
               "Webpage VARCHAR(255),"
               "Country VARCHAR(255),"
               "Region VARCHAR(255),"
               "Subdivision VARCHAR(255),"
               "Year VARCHAR(255),"
               "Garden VARCHAR(255),"
               "Price VARCHAR(255) )")

hadoop_redwine.commit()
#
# df = pd.read_csv("Redwine.csv")
# df = df.astype({col: 'string' for col in df.select_dtypes('int64').columns})
# query = (
#         "INSERT INTO bottlenbottle (Date_data,Webpage,Country,Region,Year,Price,Name,Code) "
#         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
# cursor.executemany(query, list(df.to_records(index=False)))
# hadoop_redwine.commit()
