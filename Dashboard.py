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
status_col = st.columns((3,1))
with status_col[0]:
  st.subheader('Support Ticket Status')
with status_col[1]:
  st.write(f'No. of tickets: `{len(st.session_state.df)}`')

# Status plot
st.subheader('Support Ticket Analytics')
col = st.columns((1,3,1))

with col[0]:
  n_tickets_queue = len(st.session_state.df[st.session_state.df.Status=='Open'])
  
  st.metric(label='First response time (hr)', value=5.2, delta=-1.5)
  st.metric(label='No. of tickets in the queue', value=n_tickets_queue, delta='')
  st.metric(label='Avg. ticket resolution time (hr)', value=16, delta='')
  
  
with col[1]:
  status_plot = alt.Chart(edited_df).mark_bar().encode(
      x='month(Date Submitted):O',
      y='count():Q',
      xOffset='Status:N',
      color = 'Status:N'
  ).properties(title='Ticket status in the past 6 months', height=300).configure_legend(orient='bottom', titleFontSize=14, labelFontSize=14, titlePadding=5)
  st.altair_chart(status_plot, use_container_width=True, theme='streamlit')
  
with col[2]:
  priority_plot = alt.Chart(edited_df).mark_arc().encode(
                      theta="count():Q",
                      color="Priority:N"
                  ).properties(title='Current ticket priority', height=300).configure_legend(orient='bottom', titleFontSize=14, labelFontSize=14, titlePadding=5)
  st.altair_chart(priority_plot, use_container_width=True, theme='streamlit')
