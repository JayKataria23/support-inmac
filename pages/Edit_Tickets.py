import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from st_supabase_connection import SupabaseConnection, execute_query

# Page title
st.set_page_config(page_title='Support Ticket Workflow', page_icon='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAY1BMVEX////9+PjXjI6+P0K/QkXBSErpv8D14+PJZWi6MTS7NTjFVljryMjCT1G6MjW7Njm5LTDTfoDgqaq4Jir67+/ThIbx19fz3d3doqP25+fIYGPReXvdnqDYkpP79PTluLm+QELIVu6CAAAAy0lEQVR4AX2SBQ7DQAwEHc4xlMP//2TpnNJGHbFW2pGBPsjyokxUNf3StEI+EaqBUBvrnvhAQCxkCncRsv3BplDKI4SnVrgnQmV/lAfIsrPjVlFvKLnVmgsqOw59j8q6TEppIyoHkZS2OqKy9zxIu6FU3OrHCcLZcmtZozJfW7sTKtdBxGFPRN/DHAtWuohTRs9KowkIr0FQORnBp9wYRHOrLGcCzju+iDrilKvS9nsIG7UqB0LlwsqixnCQT5zo8CL7sJRlcUd8v9YNS1IRq/svf5IAAAAASUVORK5CYII=')
st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Support Ticket Workflow')

conn = st.connection("supabase",type=SupabaseConnection)

df = execute_query(conn.table("Logs").select("*", count="None"), ttl=None)
df = pd.DataFrame(df.data)[["id", "created_at", "location", "problem", "engineer", "image", "completed", "completed_at", "call_report"]]

event =st.dataframe(df, use_container_width=True, hide_index=True, height=400, 
        on_select="rerun",
        selection_mode="single-row",)

if event.selection.rows:
        people = event.selection.rows
        filtered_df = df.iloc[people]
        filtered_df = filtered_df.reset_index()
        st.title(filtered_df["location"][0])
        st.selectbox("Created At", options=[datetime.strptime(filtered_df["created_at"][0][0:19], "%Y-%m-%dT%H:%M:%S")+timedelta(hours=5, minutes=30)])
        
        st.selectbox("ID", options=[filtered_df["id"][0]])
        st.selectbox("Location", [filtered_df["location"][0]])
        st.text_area("Issue",filtered_df["problem"][0])
        st.selectbox("Engineer", [filtered_df["engineer"][0]])
        images = filtered_df["image"][0]
        if images != None:
                for i in images:
                        data = conn.download("images" ,i, ttl=None)
                        st.image(data[0])
                        delImg = st.button("delete image", key=i)
                        if delImg:
                                images.remove(i)
                                st.rerun()
        st.file_uploader(label="Problem Images", accept_multiple_files=True, type=["png", "jpeg", "jpg", "webp"])
        st.toggle("Completed", value=filtered_df["completed"][0])
        st.date_input(label="Completed At Date", value=datetime.strptime(filtered_df["completed_at"][0][0:10], "%Y-%m-%d") if filtered_df["completed_at"][0] else None)
        st.time_input(label="Completed At Time", value=datetime.strptime(filtered_df["completed_at"][0][11:19], "%H:%M:%S")+timedelta(hours=5, minutes=30)if filtered_df["completed_at"][0] else None)
        st.file_uploader(label="Call Report", accept_multiple_files=True, type=["png", "jpeg", "jpg", "webp"])
        col1, col2 = st.columns([1,1])
        with col1:
                st.button("Save", use_container_width=True)
        with col2:
                st.button("Delete", use_container_width=True, type="primary")
        

        
