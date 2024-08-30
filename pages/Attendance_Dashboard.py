import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta


st.header("Attendance")

conn = st.connection("supabase", type=SupabaseConnection)
geolocator = Nominatim(user_agent="streamlit")

def reverse_geocode(row):
    location = geolocator.reverse((row["latitude"], row["longitude"]))
    return location.address if location else "Unknown Location"

def get_urls(row):
    url = conn.get_public_url(bucket_id="images",filepath="/"+row["image"], ttl=None)
    return url if url else "Unknown Image"

attendance_data = pd.DataFrame(execute_query(
    conn.table("attendance")
    .select("engineer_id", "latitude", "longitude", "date", "time", "image")
    .order("date", desc=True), ttl=None).data)

engineer_data = pd.DataFrame(execute_query(
    conn.table("Engineers")
    .select("id", "name"), ttl=None).data)

attendance_data = attendance_data.merge(engineer_data, left_on="engineer_id", right_on="id")
attendance_data["address"] = attendance_data.apply(reverse_geocode, axis=1)
attendance_data["url"] = attendance_data.apply(get_urls, axis=1)


date_range = st.date_input("Date Range", value=[datetime.today()-timedelta(days=30), datetime.today()])
attendance_data['date'] = pd.to_datetime(attendance_data['date'])
filtered_df = attendance_data

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0]) 
    end_date = pd.to_datetime(date_range[1]) 
    if start_date < end_date:
        filtered_df = attendance_data.loc[(attendance_data['date'] > start_date) & (attendance_data['date'] <= end_date)]
    else:
        st.error("Error: Start date is not less than end date")
else:
    st.error("Entor complete date range")

st.dataframe(filtered_df[['date', "time", 'name', "address", "url"]].reset_index(drop=True), 
                     column_config={
                    "url": st.column_config.ImageColumn("Preview Image")
                    }, use_container_width=True, hide_index=True)

df = filtered_df
df['presence'] = 'P'
pivot_df = df.pivot_table(index='name', columns=df['date'], values='presence', aggfunc='first')
pivot_df = pivot_df.fillna('A')
pivot_df = pivot_df.reset_index()
st.dataframe(pivot_df)
