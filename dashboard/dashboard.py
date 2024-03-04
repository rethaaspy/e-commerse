import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64 

# Load data
all_df = pd.read_csv("all_data.csv")

# Konversi kolom tanggal ke tipe data datetime
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Logo di sidebar
st.sidebar.image('porto.png', use_column_width=True)
st.sidebar.write('**Nama:** Retha Novianty Sipayung')
st.sidebar.write('**Email:** rethaspy91dz@gmail.com')
st.sidebar.write('**ML-79**')

# Filter tanggal
start_date = st.sidebar.date_input('Mulai', min_value=pd.to_datetime(all_df['order_purchase_timestamp']).min(), max_value=pd.to_datetime(all_df['order_purchase_timestamp']).max(), value=pd.to_datetime(all_df['order_purchase_timestamp']).min())
end_date = st.sidebar.date_input('Selesai', min_value=pd.to_datetime(all_df['order_purchase_timestamp']).min(), max_value=pd.to_datetime(all_df['order_purchase_timestamp']).max(), value=pd.to_datetime(all_df['order_purchase_timestamp']).max())

# Filter data berdasarkan tanggal
filtered_data = all_df[(all_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & (all_df['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

# Judul halaman
st.title('Dashboard Analisis E-commerce Public Data 🛒')

# Fungsi untuk mengonversi DataFrame menjadi file CSV yang dapat diunduh
def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="all_data.csv"><button>Unduh Data</button></a>'
    return href

# Tombol untuk mengunduh data CSV
st.markdown(download_csv(filtered_data), unsafe_allow_html=True)

# Tambahkan spasi antara visualisasi
st.write("")

# Pie chart - Persentase Pesanan
st.subheader('Persentase Pesananan yang Tiba Tepat Waktu dan Terlambat')
# Persentase pesanan yang tiba tepat waktu dan terlambat
percentage_on_time = (len(filtered_data[filtered_data['delivery_delay'] <= '0 days']) / len(filtered_data)) * 100
percentage_delayed = 100 - percentage_on_time
fig = px.pie(names=['Tepat Waktu', 'Terlambat'], values=[percentage_on_time, percentage_delayed])
st.plotly_chart(fig)

st.write("")
st.write("")

# Line chart - Jumlah Pesanan Terlambat per Bulan
st.subheader('Tren Pesanan Terlambat Setiap Bulan')
delayed_orders_per_month = filtered_data[pd.to_timedelta(filtered_data['delivery_delay']) > pd.Timedelta('0 days')].groupby('delivery_month').size()
fig = px.line(delayed_orders_per_month, labels={'index': 'Bulan', 'value': 'Jumlah Pesanan Terlambat'})
st.plotly_chart(fig)

# Tambahkan spasi antara visualisasi
st.write("")
st.write("")

# Tren jumlah order bulanan dari waktu ke waktu
st.subheader('Tren Jumlah Pesanan Bulanan')
monthly_orders = filtered_data.groupby('order_month').size()
fig = px.line(monthly_orders, labels={'index': 'Bulan', 'value': 'Jumlah Pesanan'})
st.plotly_chart(fig)

# Tambahkan spasi antara visualisasi
st.write("")
st.write("")

# Visualisasi distribusi geografis pelanggan
st.subheader('Distribusi Geografis Pelanggan')

#drop nilai null
filtered_data = filtered_data.dropna()

# Rename columns to match expected names
filtered_data.rename(columns={'geolocation_lat': 'LAT', 'geolocation_lng': 'LON'}, inplace=True)

# Visualisasi peta
st.map(filtered_data[['LAT', 'LON']])
