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
# Generate data
## Set seed for reproducibility
np.random.seed(42)

## Function to generate a random issue description
def generate_issue():
    issues = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications"
    ]
    return np.random.choice(issues)

## Function to generate random dates
start_date = datetime(2023, 6, 1)
end_date = datetime(2023, 12, 20)
id_values = ['TICKET-{}'.format(i) for i in range(1000, 1100)]
issue_list = [generate_issue() for _ in range(100)]


def generate_random_dates(start_date, end_date, id_values):
    date_range = pd.date_range(start_date, end_date).strftime('%m-%d-%Y')
    return np.random.choice(date_range, size=len(id_values), replace=False)

## Generate 100 rows of data
data = {'Issue': issue_list,
        'Status': np.random.choice(['Open', 'In Progress', 'Closed'], size=100),
        'Priority': np.random.choice(['High', 'Medium', 'Low'], size=100),
        'Date Submitted': generate_random_dates(start_date, end_date, id_values)
    }
df = pd.DataFrame(data)
df.insert(0, 'ID', id_values)
df = df.sort_values(by=['Status', 'ID'], ascending=[False, False])

## Create DataFrame
if 'df' not in st.session_state:
    st.session_state.df = df

# Sort dataframe
def sort_df():
    st.session_state.df = edited_df.copy().sort_values(by=['Status', 'ID'], ascending=[False, False])



recent_ticket_number = int(max(st.session_state.df.ID).split('-')[1])

status_col = st.columns((3,1))
with status_col[0]:
  st.subheader('Support Ticket Status')
with status_col[1]:
  st.write(f'No. of tickets: `{len(st.session_state.df)}`')

st.markdown('**Things to try:**')
st.info('1️⃣ Update Ticket **Status** or **Priority** and see how plots are updated in real-time!')
st.success('2️⃣ Change values in **Status** column from *"Open"* to either *"In Progress"* or *"Closed"*, then click on the **Sort DataFrame by the Status column** button to see the refreshed DataFrame with the sorted **Status** column.')

edited_df = st.data_editor(st.session_state.df, use_container_width=True, hide_index=True, height=212,
            column_config={'Status': st.column_config.SelectboxColumn(
                                        'Status',
                                        help='Ticket status',
                                        options=[
                                            'Open',
                                            'In Progress',
                                            'Closed'
                                        ],
                                        required=True,
                                        ),
                           'Priority': st.column_config.SelectboxColumn(
                                       'Priority',
                                        help='Priority',
                                        options=[
                                            'High',
                                            'Medium',
                                            'Low'
                                        ],
                                        required=True,
                                        ),
                         })
st.button('🔄 Sort DataFrame by the Status column', on_click=sort_df)

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
