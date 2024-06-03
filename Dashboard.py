import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')



st.set_page_config(page_title="Bike Sharing Dashboard",
                   page_icon="bar_chart:")

def create_cnt_year_month_df(df):
    cnt_year_month_df = df.groupby(['yr', df['dteday'].dt.month])['cnt'].sum().reset_index()
    cnt_year_month_df.columns = ['Year', 'Month', 'Total Count']
    cnt_year_month_df['Year']= cnt_year_month_df['Year'].map({0:'2011', 1: '2012'})

def create_count_season_df(df):
    count_season_df = df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
    count_season_df['season'] = count_season_df['season'].map({1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return count_season_df

def create_count_workingday_df(df):
    count_workingday_df = df.groupby("workingday").cnt.sum().sort_values(ascending=False).reset_index()
    count_workingday_df['workingday'] = count_workingday_df['workingday'].map({1: 'Workingday', 0: 'Holiday'})
    return count_workingday_df

def create_corelation_df(df):
    selected_columns =['temp', 'atemp','hum','windspeed','cnt']
    subset_df = df[selected_columns]
    corelation_df = subset_df.corr()
    return corelation_df
  
def create_hourly_df(df):
    hourly_df = df.groupby('hr')['cnt'].mean().reset_index()
    hourly_df.columns = ['Hour', 'Average Rentals']

    # Clustering hours based on whether they belong to the "busy" or "off-peak" category
    threshold = hourly_df['Average Rentals'].mean()

    def classify_by_hourly_count(value):
        if value > threshold:
            return 'Peak Hours'
        else:
            return 'Off Peak Hours'
    
    hourly_df['Hour Category'] = hourly_df['Average Rentals'].apply(classify_by_hourly_count)
  
    return hourly_df

cleaned_df = pd.read_csv("dashboard/bike_sharing_data.csv")

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
    st.image("Bike Sharing Logo.jpeg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = cleaned_df[(cleaned_df["dteday"] >= str(start_date)) & 
                (cleaned_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
count_season_df = create_count_season_df(main_df)
count_workingday_df = create_count_workingday_df(main_df)
corelation_df = create_corelation_df(main_df)
hourly_df = create_hourly_df(main_df)
cnt_year_month_df= create_cnt_year_month_df(main_df)

# MAINPAGE 
st.title("Bike Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Renters", value=total_all_rides)
with col2:
    total_day = main_df['dteday'].nunique()
    st.metric("Total Days", value=total_day)
with col3:
    rata_penyewa_perhari = total_all_rides/total_day 
    st.metric("Average Bike Renters per Day", value=rata_penyewa_perhari)

st.markdown("---")

# Plot jumlah penyewa sepeda berdasarkan musim
st.subheader("Number of bike renters per day (2011-2012)")
plt.figure(figsize=(15,5))
sns.lineplot(x='dteday', y='cnt', data=main_df)
plt.xlabel("Date")
plt.ylabel("Number of Renters")
plt.title("Number of bike renters per day (2011-2012)")
st.pyplot(plt)
    

# Plot jumlah penyewa sepeda berdasarkan musim
st.subheader("Number of Bike Renters Based on Season")
plt.figure(figsize=(10, 5))
colors = ["#1F61C4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(y="cnt", x="season", data=count_season_df, palette=colors)
plt.title("Number of Bike Renters Based on Season")
plt.ylabel("Number of Renters")
st.pyplot(plt)


# Plot jumlah penyewa sepeda berdasarkan workingday and holidays
st.subheader("Number of Bike Renters Based on Workingday")
plt.figure(figsize=(10, 5))
sns.barplot(y="cnt", x="workingday", data=count_workingday_df, palette=colors)
plt.title("Number of Bike Renters Based on Workingday")
plt.ylabel("Number of Renters")
st.pyplot(plt)

# Plot matriks korelasi dengan seaborn
st.subheader("Correlation Matrix")
plt.figure(figsize=(8, 6))
sns.heatmap(corelation_df, annot=True, cmap='Blues', vmin=-1, vmax=1)
plt.title('Correlation Matrix of temp, atemp, hum, and windspeed with the number of bike rentals')
st.pyplot(plt)

# Additional Analysis: Clustering Based on Hour
st.subheader("Analysis of Bike Renter Crowds by Hour")

# Plotting the average count per hour
plt.figure(figsize=(12, 6))
sns.lineplot(x='Hour', y='Average Rentals', data=hourly_df, marker='o', hue='Hour Category', palette=['#8CB4E1','#1F61C4'])
plt.title("Average Bike Renters by Hour with Clustering of Peak and Off-Peak Hours")
plt.xlabel("Hour")
plt.ylabel("Average Renters")
plt.legend(title='Hour Category')
plt.show()

# Highlight peak and off-peak hours based on visualization
threshold = hourly_df['Average Rentals'].mean()
peak_hours = hourly_df[hourly_df['Average Rentals'] > threshold]
off_peak_hours = hourly_df[hourly_df['Average Rentals'] <= threshold]

st.markdown("### Peak Hour Cluster")
st.dataframe(peak_hours)

st.markdown("### Off-Peak Hour Cluster")
st.dataframe(off_peak_hours)


st.caption('Copyright (c), created by M. Wahyu Abdila Lubis')
