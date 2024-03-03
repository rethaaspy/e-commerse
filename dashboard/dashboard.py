import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64 

# Load data
all_df = pd.read_csv("all_data.csv")

# Logo di sidebar
st.sidebar.image('porto.png',use_column_width=True)
st.sidebar.write('**Nama:** Retha Novianty Sipayung')
st.sidebar.write('**Email:** rethaspy91dz@gmail.com')
st.sidebar.write('**ML-79**')

# Judul halaman
st.title('Dashboard Analisis E-commerce Public Data 🛒')


# Fungsi untuk mengonversi DataFrame menjadi file CSV yang dapat diunduh
def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="all_data.csv"><button>Unduh Data</button></a>'
    return href

# Tombol untuk mengunduh data CSV
st.markdown(download_csv(all_df), unsafe_allow_html=True)


# Tambahkan spasi antara visualisasi
st.write("")

# Pie chart - Persentase Pesanan
st.subheader('Persentase Pesananan yang Tiba Tepat Waktu dan Terlambat')
# Persentase pesanan yang tiba tepat waktu dan terlambat
percentage_on_time = (len(all_df[all_df['delivery_delay'] <= '0 days']) / len(all_df)) * 100
percentage_delayed = 100 - percentage_on_time
fig = px.pie(names=['Tepat Waktu', 'Terlambat'], values=[percentage_on_time, percentage_delayed])
st.plotly_chart(fig)

st.write("")
st.write("")

# Line chart - Jumlah Pesanan Terlambat per Bulan
st.subheader('Tren Pesanan Terlambat Setiap Bulan')
delayed_orders_per_month = all_df[pd.to_timedelta(all_df['delivery_delay']) > pd.Timedelta('0 days')].groupby('delivery_month').size()
fig = px.line(delayed_orders_per_month, labels={'index': 'Bulan', 'value': 'Jumlah Pesanan Terlambat'})
st.plotly_chart(fig)

# Tambahkan spasi antara visualisasi
st.write("")
st.write("")

# Tren jumlah order bulanan dari waktu ke waktu
st.subheader('Tren Jumlah Pesanan Bulanan')
monthly_orders = all_df.groupby('order_month').size()
fig = px.line(monthly_orders, labels={'index': 'Bulan', 'value': 'Jumlah Pesanan'})
st.plotly_chart(fig)

# Tambahkan spasi antara visualisasi
st.write("")
st.write("")

# Visualisasi distribusi geografis pelanggan
st.subheader('Distribusi Geografis Pelanggan')
fig = px.scatter(all_df, x='geolocation_lng', y='geolocation_lat', labels={'geolocation_lng': 'Longitude', 'geolocation_lat': 'Latitude'})
st.plotly_chart(fig)
