import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

# ==============================
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    return daily_orders_df

def create_payment_type_df(df):
    payment_df = df.groupby('payment_type').agg({
        'order_id': 'count',
        'payment_value': 'mean'
    }).reset_index()
    return payment_df.sort_values(by='order_id', ascending=False)

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bystate_df.sort_values(by="customer_count", ascending=False)

def create_rfm_df(df):
    recent_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    rfm_df = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()
    rfm_df.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']
    
    # Segmentasi
    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 4, labels=[4, 3, 2, 1])
    rfm_df['F_Score'] = rfm_df['Frequency'].apply(lambda x: 4 if x > 2 else (3 if x == 2 else 1))
    rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 4, labels=[1, 2, 3, 4])
    
    def segment_customer(df_row):
        if df_row['R_Score'] == 4 and df_row['F_Score'] >= 3 and df_row['M_Score'] >= 3: 
            return 'Champions'
        elif df_row['R_Score'] >= 3: 
            return 'Recent Customers'
        elif df_row['R_Score'] == 1 and df_row['F_Score'] == 1: 
            return 'Lost Customers'
        else: 
            return 'Regular Customers'
            
    rfm_df['Customer_Segment'] = rfm_df.apply(segment_customer, axis=1)
    return rfm_df

all_df = pd.read_csv("main_data.csv")

# Mengubah tipe data tanggal
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# Mengurutkan data berdasarkan tanggal
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Mendapatkan tanggal minimum dan maksimum untuk filter
min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

# ==============================
with st.sidebar:
    # Menambahkan Logo E-Commerce
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.write("### E-Commerce Data Filter")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataset utama berdasarkan rentang waktu yang dipilih
main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                 (all_df["order_purchase_timestamp"].dt.date <= end_date)]

# Memanggil Helper Functions dengan data yang sudah difilter
daily_orders_df = create_daily_orders_df(main_df)
payment_type_df = create_payment_type_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# ==============================
st.header('E-Commerce Public Dashboard')

# 1. Daily Orders Section
st.subheader('Daily Orders & Revenue')
col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df['order_count'].sum()
    st.metric("Total Orders", value=f"{total_orders:,}")
with col2:
    total_revenue = daily_orders_df['revenue'].sum()
    st.metric("Total Revenue", value=f"R$ {total_revenue:,.2f}")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_orders_df["order_purchase_timestamp"], daily_orders_df["order_count"], marker='o', linewidth=2, color="#90CAF9")
ax.set_ylabel("Order Count", fontsize=15)
ax.set_xlabel("Date", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12, rotation=45)
st.pyplot(fig)

# 2. Preferensi Pembayaran
st.subheader('Payment Method Preference')
fig, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=payment_type_df, x='payment_type', y='order_id', color='#90CAF9', ax=ax1)
ax1.set_ylabel('Jumlah Transaksi', color='blue')
ax1.set_xlabel('Tipe Pembayaran')
ax2 = ax1.twinx()
sns.lineplot(data=payment_type_df, x='payment_type', y='payment_value', color='red', marker='o', ax=ax2)
ax2.set_ylabel('Rata-rata Nilai Transaksi (Red Line)', color='red')
st.pyplot(fig)

# 3. Demografi Geografis
st.subheader('Customer Demographics by State')
fig, ax = plt.subplots(figsize=(12, 6))
colors = ["#90CAF9" if i == 0 else "#D3D3D3" for i in range(10)]
sns.barplot(data=bystate_df.head(10), x='customer_count', y='customer_state', palette=colors, ax=ax)
ax.set_title("Top 10 States by Number of Customers", loc="center", fontsize=15)
ax.set_ylabel("State")
ax.set_xlabel("Number of Customers")
st.pyplot(fig)

# 4. RFM Analysis Section
st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.Recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.Frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
with col3:
    avg_monetary = round(rfm_df.Monetary.mean(), 2)
    st.metric("Average Monetary", value=f"R$ {avg_monetary:,.2f}")

fig, ax = plt.subplots(figsize=(10, 5))
segment_counts = rfm_df['Customer_Segment'].value_counts().reset_index()
sns.barplot(data=segment_counts, x='count', y='Customer_Segment', palette='viridis', ax=ax)
ax.set_title('Customer Segmentation Distribution', fontsize=15)
ax.set_xlabel('Number of Customers')
ax.set_ylabel('Segment')
st.pyplot(fig)

st.caption('Copyright (c) E-Commerce Data Analytics 2024')