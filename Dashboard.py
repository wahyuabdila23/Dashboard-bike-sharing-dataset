import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

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

def classify_peak_hours(df, threshold):
    df['is_peak'] = (df['cnt'] > threshold).astype(int)
    features = ['hr']
    X = df[features]
    y = df['is_peak']
    return X, y

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
    st.image("Bike Sharing Logo.jpeg")
    
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
corelation_df = create_corelation_df(main_df)

# MAINPAGE 
st.title("Bike Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Penyewa", value=total_all_rides)
with col2:
    total_day = main_df['dteday'].nunique()
    st.metric("Total Hari", value=total_day)
with col3:
    rata_penyewa_perhari = total_all_rides/total_day 
    st.metric("Rata-rata Penyewa sepeda Perhari", value=rata_penyewa_perhari)

st.markdown("---")


# plot number of daily orders (2021)
st.header('Bike Sharing Dashboard :sparkles:')

# Plot jumlah penyewa sepeda berdasarkan musim
st.subheader("Grafik Penyewa Sepeda 2011-2012")
plt.figure(figsize=(15,5))
sns.lineplot(x='dteday', y='cnt', data=main_df)
plt.xlabel("Hari")
plt.ylabel("Jumlah Penyewa")
plt.title("Jumlah penyewa sepeda per hari(2011-2012)")
st.pyplot(plt)
    

# Plot jumlah penyewa sepeda berdasarkan musim
st.subheader("Jumlah Penyewa Sepeda Berdasarkan Musim")
plt.figure(figsize=(10, 5))
colors = ["#1F77B4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(y="cnt", x="season", data=count_season_df, palette=colors)
plt.title("Jumlah Penyewa Sepeda Berdasarkan Musim")
plt.ylabel("Jumlah Penyewa")
st.pyplot(plt)


# Plot jumlah penyewa sepeda berdasarkan musim
st.subheader("Jumlah Penyewa Sepeda Berdasarkan Workingday")
plt.figure(figsize=(10, 5))
sns.barplot(y="cnt", x="workingday", data=count_workingday_df, palette=colors)
plt.title("Jumlah Penyewa Sepeda Berdasarkan Workingday")
plt.ylabel("Jumlah Penyewa")
st.pyplot(plt)

# Plot matriks korelasi dengan seaborn
st.subheader("Korelasi suhu dengan total penyewa")
plt.figure(figsize=(8, 6))
sns.heatmap(corelation_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matriks Korelasi')
st.pyplot(plt)


# Additional Analysis: Classification for Peak Hours
st.subheader("Klasifikasi Jam Ramai Penyewa")

# Define threshold for peak hours
threshold = main_df['cnt'].quantile(0.75)

# Prepare data for classification
X, y = classify_peak_hours(main_df, threshold)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predictions and Evaluation
y_pred = clf.predict(X_test)

st.markdown("#### Classification Report")
st.text(classification_report(y_test, y_pred))

st.markdown("#### Confusion Matrix")
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap='coolwarm')
plt.xlabel("Predicted")
plt.ylabel("Actual")
st.pyplot(plt)

st.markdown("#### Feature Importances")
feature_importances = pd.Series(clf.feature_importances_, index=X.columns)
sns.barplot(x=feature_importances, y=feature_importances.index)
plt.title("Feature Importances")
st.pyplot(plt)
