import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency
sns.set(style='dark')

dailybs_df = pd.read_csv("https://raw.githubusercontent.com/ahmadziyanfm/Dataset-Dicoding-Ziyan/main/day.csv")
# Membuat dictionary yang memetakan nilai lama ke nilai baru
season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

# Mengganti nilai kolom 'season' menggunakan metode replace dengan dictionary
dailybs_df['season'] = dailybs_df['season'].replace(season_mapping)
dailybs_df['weekday'] = dailybs_df['weekday'].replace(day_mapping)

all_df = dailybs_df.copy()

all_df['dteday']=pd.to_datetime(all_df['dteday'])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/ahmadziyanfm/Dataset-Dicoding-Ziyan/blob/030782f2c320a42aacc8d87b99d00603c68cf210/fitursewasepedafix.png?raw=true")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "instant": "count_day",
        "cnt": "count_rent"
    }, inplace=True)
    
    return daily_orders_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season")["cnt"].sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "total_cnts"
    }, inplace=True)
    
    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit")["cnt"].sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "total_cntw"
    }, inplace=True)
    
    return byweather_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit")["cnt"].sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "total_cntw"
    }, inplace=True)
    
    return byweather_df

def create_byday_df(df):
    byday_df = df.groupby(by="weekday")["cnt"].sum().reset_index()
    byday_df.rename(columns={
        "cnt": "total_cntwk"
    }, inplace=True)
    
    return byday_df

# Mendefinisikan data pilihan hasil filter
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Grafik Line Chart 
daily_orders_df = create_daily_orders_df(main_df)

st.header('Bike Rental Dashboard :sparkles::bike:')

st.subheader('Daily Count')
 
col1, col2 = st.columns(2)
 
with col1:
    total_days = daily_orders_df.count_day.sum()
    st.metric("Total Days", value=total_days)
 
with col2:
    total_rent = daily_orders_df.count_rent.sum() 
    st.metric("Total Rental Bikes", value=total_rent)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["count_rent"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Grafik pie chart

st.subheader('Count of Rental Bikes by Season & Weather')
 
col1, col2 = st.columns(2)
 
with col1:
  daily_season_df = create_byseason_df(main_df)
  # Konfigurasi plot
  fig, ax = plt.subplots()
  ax.pie(daily_season_df['total_cnts'], labels=daily_season_df['season'], autopct='%1.1f%%', startangle=90)
  ax.axis('equal')  # Aspek rasio lingkaran

  # Menampilkan plot menggunakan Streamlit
  st.write("""## <span style='font-size:17px;font-weight:bold;'>by Season</span>""", unsafe_allow_html=True)
  st.pyplot(fig)

with col2:
  daily_weather_df = create_byweather_df(main_df)
  
# Membuat donut chart dengan Matplotlib
  colorsd = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
  plt.figure(figsize=(7, 7))
  plt.pie(daily_weather_df['total_cntw'], labels=daily_weather_df['weathersit'], colors=colorsd, autopct='%1.1f%%', startangle=90)
  centre_circle = plt.Circle((0,0),0.70,fc='white')
  fig = plt.gcf()
  fig.gca().add_artist(centre_circle)
  plt.title('by Weather')
  plt.axis('equal')  

# Menampilkan donut chart di Streamlit
  st.pyplot(plt)
# Menampilkan donut chart di samping keterangan
col1, col2 = st.columns([2,1])
  
with col1:
    " "
# Menampilkan keterangan di samping grafik
with col2:
    st.write("""
    Keterangan:
    - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
    - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
    - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
    - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
    """)

# Membuat barplot
st.subheader('Count of Rental Bikes by Day')

daily_day_df = create_byday_df(main_df)
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="total_cntwk", 
    y="weekday",
    data=daily_day_df.sort_values(by="total_cntwk", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Count of Total Rental Bikes by Day", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

