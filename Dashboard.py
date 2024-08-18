import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from st_supabase_connection import SupabaseConnection, execute_query

# Page title
st.set_page_config(page_title='Support Ticket Workflow', page_icon='data:image/png;base64,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')
st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Support Ticket Workflow')

conn = st.connection("supabase",type=SupabaseConnection)

df = execute_query(conn.table("Logs").select("*", count="None"), ttl="0")

if len(df.data) > 0:
  df = pd.DataFrame(df.data)
  status_col = st.columns((3,1))
  with status_col[0]:
    st.subheader('Support Ticket Analysis')
  with status_col[1]:
    st.write(f'No. of tickets: `{len(df)}`')

  col1, col2, col3 = st.columns(3)
  num_open_tickets = len(df[df["completed"] == False]) 
  num_completed_tickets = len(df[df["completed"] == True]) 
  delta_open = len(df[df["created_at"] == datetime.today()])
  delta_completed = len(df[df["completed_at"] == datetime.today()])
  col1.metric(label="Number of open tickets", value=num_open_tickets, delta=delta_open)
  col2.metric(label="Number of closed tickets", value=num_completed_tickets, delta=delta_completed)
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
