from sqlalchemy import create_engine
import pandas as pd
import pymysql
import functools
import operator
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from scipy.cluster.vq import kmeans

#######################################################################################
@st.cache
def load_all_data():
    db_connection_str = 'mysql+pymysql://root:joniwhfe@34.92.69.178/Redwine_testing'
    db_connection = create_engine(db_connection_str)
    df = pd.read_sql('SELECT * FROM Redwine_testing', con=db_connection)
    return df

#######################################################################################
def date_price_mean(France_wine):
    date_price = France_wine.groupby(['Date', 'Webpage'],as_index=False).size()
    fig = plt.figure(figsize=(15, 10))
    sns.barplot(x="Date", y="size", hue="Webpage", data=date_price)
    st.pyplot(fig)

def show_metric(winemap,winecouple):
    st.subheader('Year v.s. Inventory')
    winemap_rows = winemap.shape[0]
    winecouple_rows = winecouple.shape[0]
    col1, col2= st.columns(2)
    col1.metric("Winemap", winemap_rows)
    col2.metric("Winecouple", winecouple_rows)

def barchart_type(Red_testing_df):
    st.subheader('Region v.s. Inventory')
    Type = Red_testing_df.groupby(['Webpage', 'Region'],as_index=False).size()
    st.table(Type)
    fig = plt.figure(figsize=(15, 5))
    sns.barplot(x="Webpage", y="size", hue="Region", data=Type)
    st.pyplot(fig)

def selectbox_garden(winemap,winecouple):
    st.subheader('Garden of Wines')
    Garden_map =  winemap['Garden'].unique()
    option = st.selectbox('The Garden Name of Winemap?',Garden_map)
    st.write('You selected:', option)
    st.table(winemap[winemap['Garden']==option])
    Garden_couple =  winecouple['Garden'].unique()
    option_02 = st.selectbox('The Garden Name of Winecouple?',Garden_couple)
    st.write('You selected:', option_02)
    st.table(winecouple[winecouple['Garden']==option_02])

def year_barchart(Red_testing_df):
    Year = Red_testing_df.groupby(['Year', 'Webpage'], as_index=False).size()
    fig = plt.figure(figsize=(20, 10))
    sns.barplot(x="Year", y="size", hue="Webpage", data=Year)
    st.pyplot(fig)

def join_table(winemap,winecouple):
    st.subheader('Cheapest website for a Wine')
    winemap = winemap[['Date','Garden','Year','Webpage','Price']]
    winecouple = winecouple[['Date','Garden','Year','Webpage','Price']]
    comparison = winemap.merge(winecouple, left_on=["Garden",'Year'], right_on=["Garden",'Year'])
    comparison = comparison.drop(['Date_y'], axis=1)
    st.table(comparison)

def year_price(Red_testing_df):
    st.subheader('Production Year vs Price(median)')
    price_median = []
    year_unique = Red_testing_df['Year'].sort_values().unique()
    for elements in year_unique:
        median_price = int(Red_testing_df[Red_testing_df['Year']==elements]['Price'].median())
        price_median.append(median_price)
    year_unique = year_unique.tolist()
    year_price_median = pd.DataFrame({
                    'Year':year_unique,
                    'Price':price_median
                 })
    fig = plt.figure(figsize=(20, 10))
    sns.lineplot(x="Year", y="Price", data=year_price_median)
    st.pyplot(fig)

def winemap_range(wine):
    wine_price = wine['Price']
    wine_price = wine_price.astype(int)
    wine_median = int(wine_price.median())
    wine_max = wine_price.max()
    wine_min = wine_price.min()
    col1, col2, col3 = st.columns(3)
    col1.metric("Median", wine_median)
    col2.metric("Max", wine_max)
    col3.metric("Min", wine_min)

def clustering(Red_testing_df):
    price = Red_testing_df['Price'].astype(float)
    x = range(len(price))
    m = np.matrix([x, price]).transpose()
    print(m)
    kclust = kmeans(m, 3)
    clustering_point = np.sort(kclust[0][:, 1]).astype(int)
    st.subheader("Clustering by Kmeans")
    col1, col2, col3,col4 = st.columns(4)
    col1.metric("Cluster 1", clustering_point[0])
    col2.metric("Cluster 2", clustering_point[1])
    col3.metric("Cluster 3", clustering_point[2])
    col4.metric("Deviation", kclust[1].astype(int))

def correlation_year_price(Red_testing_df):
    st.subheader("Correlation")
    st.table(Red_testing_df[['Year', 'Price']].astype(int).corr())

def linear_regression_year_price(Red_testing_df):
    st.subheader("Linear regression")
    fig = plt.figure(figsize=(15, 10))
    sns.regplot(x="Year", y="Price", data=Red_testing_df[["Year", "Price"]].astype(int), scatter_kws={"s": 0.1},line_kws={"color": "red"})
    st.pyplot(fig)
#######################################################################################

France_wine = load_all_data()
France_wine['Date'] = pd.to_datetime(France_wine.Date, format='%Y-%m-%d')
France_wine['Date'] = France_wine["Date"].dt.strftime("%Y-%m-%d")
latest_date = France_wine['Date'].max()


st.title("France_Redwine")

France_wine_today = France_wine[France_wine['Date']==latest_date]
winemap = France_wine[France_wine['Webpage'] == 'Winemap']
winecouple = France_wine[France_wine['Webpage'] == 'Winecouple']

add_selectbox = st.sidebar.selectbox("Redwine_type",("Gross_Date","Today", "Winemap", "Winecouple","Machine Learning"))


if add_selectbox == 'Gross_Date':
    st.subheader("Raw data")
    st.write(France_wine)
    date_price_mean(France_wine)

elif add_selectbox == 'Today':
    st.subheader("Today raw data")
    if st.checkbox(label="Show raw data"):
        st.write(France_wine_today)
    st.subheader('Inventory')
    show_metric(winemap,winecouple)
    year_barchart(France_wine)
    barchart_type(France_wine)
    selectbox_garden(winemap, winecouple)
    join_table(winemap, winecouple)
    year_price(France_wine)
elif add_selectbox == 'Winemap':
     st.write(winemap)
     st.subheader("Winemap")
     winemap_range(winemap)

elif add_selectbox == 'Winecouple':
     st.write(winecouple)
     st.subheader("Winecouple")
     winemap_range(winecouple)

elif add_selectbox == "Machine Learning":
    clustering(France_wine)
    correlation_year_price(France_wine)
    linear_regression_year_price(France_wine)