import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Import data
hour_df = pd.read_csv("https://github.com/wahyuabdila23/Dashboard-bike-sharing-dataset/blob/main/all_data.csv")

# Data Cleaning
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
hour_df.drop(columns=["instant", "holiday"], inplace=True)

# Defining Business Questions
questions = {
    "Trend Peminjaman Sepeda (2011-2012)": "Bagaimana tren peminjaman sepeda berubah dari tahun 2011 ke tahun 2012?",
    "Peminjaman Sepeda Berdasarkan Musim": "Bagaimana distribusi peminjaman sepeda berbeda di musim semi, panas, gugur, dan musim dingin?",
    "Jumlah Peminjaman Sepeda pada Hari Kerja vs Hari Libur": "Apakah jumlah peminjaman sepeda lebih tinggi pada hari kerja atau hari libur?",
    "Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda": "Bagaimana pengaruh suhu terhadap jumlah peminjaman sepeda?"
}

# Sidebar
st.sidebar.title("Business Questions")
selected_question = st.sidebar.selectbox("Select a question", list(questions.keys()))

# Main Content
st.title("Bike Sharing Analysis Dashboard")

if selected_question == "Trend Peminjaman Sepeda (2011-2012)":
    st.header("Trend Peminjaman Sepeda (2011-2012)")
    plt.figure(figsize=(15, 5))
    sns.lineplot(x='dteday', y='cnt', data=hour_df)
    plt.xlabel("Date")
    plt.ylabel("Number of Rentals")
    plt.title("Number of Bike Rentals per Day (2011-2012)")
    st.pyplot()

elif selected_question == "Peminjaman Sepeda Berdasarkan Musim":
    st.header("Peminjaman Sepeda Berdasarkan Musim")
    cnt_season = hour_df.groupby("season")['cnt'].sum().sort_values(ascending=False).reset_index()
    cnt_season['season'] = cnt_season['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

    plt.figure(figsize=(10, 5))
    sns.barplot(y="cnt", x="season", data=cnt_season)
    plt.title("Number of Bike Rentals by Season")
    plt.ylabel("Number of Rentals")
    plt.xlabel("Season")
    st.pyplot()

elif selected_question == "Jumlah Peminjaman Sepeda pada Hari Kerja vs Hari Libur":
    st.header("Jumlah Peminjaman Sepeda pada Hari Kerja vs Hari Libur")
    cnt_holiday = hour_df.groupby("workingday")['cnt'].sum().sort_values(ascending=False).reset_index()
    cnt_holiday['workingday'] = cnt_holiday['workingday'].map({1: 'Workingday', 0: 'Holiday'})

    plt.figure(figsize=(8, 5))
    sns.barplot(x='workingday', y='cnt', data=cnt_holiday)
    plt.title("Number of Bike Rentals by Workingday")
    plt.xlabel("")
    plt.ylabel("Number of Rentals")
    st.pyplot()

elif selected_question == "Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda":
    st.header("Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda")
    correlation_matrix = hour_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix')
    st.pyplot()

st.caption('Copyright © Your Company')
