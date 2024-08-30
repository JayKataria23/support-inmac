import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import pandas as pd
from geopy.geocoders import Nominatim

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
location = geolocator.reverse("19.1616612, 72.8503479")
attendance_data["address"] = attendance_data.apply(reverse_geocode, axis=1)
attendance_data["url"] = attendance_data.apply(get_urls, axis=1)
# attendance_data["image"] = attendance_data.apply(get_urls, axis=1)
event = st.dataframe(attendance_data[['date', "time", 'name', "address", "url"]].reset_index(drop=True), 
                     column_config={
                    "url": st.column_config.ImageColumn("Preview Image")
                    }, use_container_width=True, hide_index=True)


df = attendance_data
df['presence'] = 'P'
pivot_df = df.pivot_table(index='name', columns=df['date'], values='presence', aggfunc='first')
pivot_df = pivot_df.fillna('A')
pivot_df = pivot_df.reset_index()
st.dataframe(pivot_df)
