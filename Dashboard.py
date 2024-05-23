import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul untuk aplikasi Streamlit
st.title("Dashboard Penyewaan Sepeda")

# Membaca dataset
data = pd.read_csv("all_data.csv")

# Konversi kolom "dteday" menjadi tipe data datetime
data["dteday"] = pd.to_datetime(data["dteday"])

# Plot jumlah penyewa sepeda per hari
st.header("Jumlah Penyewa Sepeda per Hari (2011-2012)")
plt.figure(figsize=(15, 5))
sns.lineplot(x='dteday', y='cnt', data=data)
plt.xlabel("Hari")
plt.ylabel("Jumlah Penyewa")
plt.title("Jumlah Penyewa Sepeda per Hari (2011-2012)")
st.pyplot()

# Grup berdasarkan tahun
cnt_year = data.groupby("yr").cnt.sum().sort_values(
    ascending=False).reset_index()

# Grup berdasarkan musim
cnt_season = data.groupby("season").cnt.sum(
).sort_values(ascending=False).reset_index()

# Grup berdasarkan hari kerja
cnt_holiday = data.groupby("workingday").cnt.sum(
).sort_values(ascending=False).reset_index()

# Plot jumlah penyewa sepeda berdasarkan musim
st.header("Jumlah Penyewa Sepeda Berdasarkan Musim")
plt.figure(figsize=(10, 5))
sns.barplot(y="cnt", x="season", data=cnt_season.sort_values(
    by="cnt", ascending=False))
plt.title("Jumlah Penyewa Sepeda Berdasarkan Musim")
plt.ylabel("Jumlah Penyewa")
plt.xticks([0, 1, 2, 3], ['Semi', 'Panas', 'Gugur', 'Salju'])
plt.xlabel("Musim")
st.pyplot()

# Plot jumlah penyewa sepeda berdasarkan hari kerja atau tidak
st.header("Jumlah Penyewa Sepeda Berdasarkan Hari Libur atau Tidak")
plt.figure(figsize=(10, 5))
sns.barplot(y="cnt", x="workingday",
            data=cnt_holiday.sort_values(by="cnt", ascending=False))
plt.title("Jumlah Penyewa Sepeda Berdasarkan Hari Libur atau Tidak")
plt.ylabel("Jumlah Penyewa")
plt.xticks([0, 1], ['Hari Libur', 'Hari Kerja'])
plt.xlabel("Hari Libur atau Tidak")
st.pyplot()

# Matriks korelasi
st.header("Matriks Korelasi")
selected_columns = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
subset_df = data[selected_columns]
correlation_matrix = subset_df.corr()

# Plot matriks korelasi dengan seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matriks Korelasi')
st.pyplot()
