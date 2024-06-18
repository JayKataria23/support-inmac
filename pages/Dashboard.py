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

        status_col = st.columns((2, 2))
        st.write("==ID==", filtered_df["id"][0])
        st.write("**Created At**", filtered_df["created_at"][0])
