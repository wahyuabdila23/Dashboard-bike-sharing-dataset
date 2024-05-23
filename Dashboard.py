import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

def create_count_season_df(df):
    count_season_df = df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
    return count_season_df

def create_count_workingday_df(df):
    count_workingday_df = df.groupby("workingday").cnt.sum().sort_values(ascending=False).reset_index()
    return count_workingday_df

cleaned_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
cleaned_df.sort_values(by="dteday", inplace=True)
cleaned_df.reset_index(inplace=True)

for column in datetime_columns:
    cleaned_df[column] = pd.to_datetime(cleaned_df[column])

# Filter data
min_date = cleaned_df["dteday"].min()
max_date =cleaned_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = cleaned_df[(cleaned_df["dteday"] >= str(start_date)) & 
                (cleaned_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
count_season_df = create_count_season_df(main_df)
count_workingday_df = create_count_workingday_df(main_df)


# plot number of daily orders (2021)
st.header('Bike Sharing Dashboard :sparkles:')
    

# Plot jumlah penyewa sepeda berdasarkan musim
st.header("Jumlah Penyewa Sepeda Berdasarkan Musim")
plt.figure(figsize=(10, 5))
sns.barplot(y="cnt", x="season", data=count_season_df.sort_values(
    by="cnt", ascending=False))
plt.title("Jumlah Penyewa Sepeda Berdasarkan Musim")
plt.ylabel("Jumlah Penyewa")
plt.xlabel("Musim")
st.pyplot(plt)
