import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from st_supabase_connection import SupabaseConnection, execute_query

# Page title

st.set_page_config(page_title='Support Ticket Workflow', page_icon="https://inmac.co.in/wp-content/uploads/2023/08/cropped-ms-icon-310x310-1-32x32.png")
st.image("https://inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png")
st.title( 'Support Ticket Workflow')

conn = st.connection("supabase",type=SupabaseConnection)

df = execute_query(conn.table("Logs").select("*", count="None"), ttl="0")

if len(df.data) > 0:
  df = pd.DataFrame(df.data)
  status_col = st.columns((3,1))
  with status_col[0]:
    st.subheader('Support Ticket Analysis')
  


  placeholder = st.empty()
  
  date_range = st.date_input("Date Range", value=[datetime.today()-timedelta(days=30), datetime.today()])
  df['created_at']= pd.to_datetime(df['created_at'], format='ISO8601').dt.date
  filtered_df = df

  if len(date_range) == 2:
    start_date = date_range[0]
    end_date = date_range[1]
    if start_date < end_date:
      filtered_df = df.loc[(df['created_at'] > start_date) & (df['created_at'] <= end_date)]
    else:
      st.error("Error: Start date is not less than end date")
  else:
    st.error("Entor complete date range")

  with placeholder:
    with status_col[1]:
      st.write(f'No. of tickets: `{len(filtered_df)}`')
    col1, col2, col3 = st.columns(3)
    num_open_tickets = len(filtered_df[filtered_df["completed"] == False]) 
    num_completed_tickets = len(filtered_df[filtered_df["completed"] == True]) 
    delta_open = len(filtered_df[filtered_df["created_at"] == datetime.today()])
    delta_completed = len(filtered_df[filtered_df["completed_at"] == datetime.today()])
    col1.metric(label="Number of open tickets", value=num_open_tickets, delta=delta_open)
    col2.metric(label="Number of closed tickets", value=num_completed_tickets, delta=delta_completed)

  colA, colB = st.columns(2)
  complete = colA.selectbox("Completed Status", options=["Completed", "Not Completed", "All"], index=2)
  paused = colB.selectbox("Pause Status", options=["Paused", "Active", "All"], index=2)
  if complete != "All":
    if complete == "Completed":
      filtered_df= filtered_df[filtered_df["completed"] == True]
    else:
      filtered_df= filtered_df[filtered_df["completed"] == False]
  # if paused != "All":
  #   if paused == "Paused":
  #     filtered_df= filtered_df[len(filtered_df["activeTime"])%2 == 0]
  #   else:
  #     filtered_df= filtered_df[len(filtered_df["activeTime"])%2 == 1]


  engineer = st.multiselect("Engineer", options=df["engineer"].unique())
  if len(engineer)!=0:
    filtered_df= filtered_df[filtered_df["engineer"].isin(engineer)]
  
  location = st.multiselect("Location", options=df["location"].unique())
  if len(location)!=0:
    filtered_df= filtered_df[filtered_df["location"].isin(location)]

  st.write("### Tickets")
  status_plot = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x=alt.X("yearmonthdate(created_at)", axis=alt.Axis(title='Days')) ,
        y="count():Q",
        xOffset="priority:N",
        color=alt.Color("priority:N", scale=alt.Scale(domain=['Low', 'Medium', 'High'], range=['#0096FF', '#ff7f0e', 'red']), legend=alt.Legend(title="Priority")),
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
  )
  st.altair_chart(status_plot, use_container_width=True, theme="streamlit")
  st.write("##### Current ticket priorities")
  priority_plot = (
      alt.Chart(filtered_df)
      .mark_arc()
      .encode(theta="count():Q",
        color=alt.Color("priority:N", scale=alt.Scale(domain=['Low', 'Medium', 'High'], range=['#0096FF', '#ff7f0e', 'red']), legend=alt.Legend(title="Priority")),
    )
      .properties(height=300)
      .configure_legend(
          orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
      )
  )
  st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")

  filtered_df2 = filtered_df
  filtered_df2["comp"] = np.where(filtered_df2["completed"]==True, "Completed", "Not Completed")
  st.write("### Tickets")
  complete_plot2 = (
    alt.Chart(filtered_df2)
    .mark_bar()
    .encode(
        x=alt.X("yearmonthdate(created_at):O", axis=alt.Axis(title='Days')) ,
        y="count():Q",
        xOffset="comp:N",
        color=alt.Color("comp", scale=alt.Scale(domain=['Completed','Not Completed'], range=['#0096FF', 'red']), legend=alt.Legend(title="Completed")),
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
  )
  st.altair_chart(complete_plot2, use_container_width=True, theme="streamlit")
  st.write("##### Current ticket progress")
  complete_plot = (
      alt.Chart(filtered_df2)
      .mark_arc()
      .encode(theta="count():Q",
        color=alt.Color("comp:N", scale=alt.Scale(domain=['Completed','Not Completed'], range=['#0096FF', 'red']), legend=alt.Legend(title="Priority")),
    )
      .properties(height=300)
      .configure_legend(
          orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
      )
  )
  st.altair_chart(complete_plot, use_container_width=True, theme="streamlit")
  filtered_df3 = filtered_df[["id", "created_at", "location", "priority", "problem", "engineer", "image","completed", "completed_at", "call_report", "serialNumbers"]]
  st.dataframe(filtered_df3, use_container_width=True, hide_index=True, height=400, 
                on_select="rerun",
                selection_mode="single-row",column_config={
                        "id":"ID",
                        "created_at":st.column_config.DatetimeColumn("Created At"),
                        "location":"Company - Branch",
                        "priority":"Priority",
                        "problem":"Problem Statement",
                        "engineer":"Engineer Name",
                        "image":st.column_config.ListColumn("Images"),
                        "completed":st.column_config.CheckboxColumn("Completed"),
                        "completed_at":st.column_config.DatetimeColumn("Completed At"),
                        "call_report":st.column_config.ListColumn("Call Reports"), 
                        "serialNumbers":st.column_config.ListColumn("Serial Numbers"), 
                })
