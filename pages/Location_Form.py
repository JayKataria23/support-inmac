import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query


conn = st.connection("supabase",type=SupabaseConnection)

st.set_page_config(page_title='Support Ticket Workflow', page_icon='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAY1BMVEX////9+PjXjI6+P0K/QkXBSErpv8D14+PJZWi6MTS7NTjFVljryMjCT1G6MjW7Njm5LTDTfoDgqaq4Jir67+/ThIbx19fz3d3doqP25+fIYGPReXvdnqDYkpP79PTluLm+QELIVu6CAAAAy0lEQVR4AX2SBQ7DQAwEHc4xlMP//2TpnNJGHbFW2pGBPsjyokxUNf3StEI+EaqBUBvrnvhAQCxkCncRsv3BplDKI4SnVrgnQmV/lAfIsrPjVlFvKLnVmgsqOw59j8q6TEppIyoHkZS2OqKy9zxIu6FU3OrHCcLZcmtZozJfW7sTKtdBxGFPRN/DHAtWuohTRs9KowkIr0FQORnBp9wYRHOrLGcCzju+iDrilKvS9nsIG7UqB0LlwsqixnCQT5zo8CL7sJRlcUd8v9YNS1IRq/svf5IAAAAASUVORK5CYII=')
st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Add Location to DB')

with st.form('location'):
    location = st.text_input('Company - Branch*', )
    address = st.text_area('Address*')
    pincode = st.text_input('Pincode*')
    contact_name = st.text_input('Contact Person Name*')
    contact_number = st.text_input('Contact Number*')
    email = st.text_input('Email ID*')
    submit = st.form_submit_button('Submit')

    if submit:
        if location != "" and address != "" and pincode != "" and contact_name != "" and contact_number != "" and email !="":
            st.write("Location Saving")
            execute_query(conn.table('Locations').insert([{"name":location,
                                                           "address":address,
                                                           "pincode":pincode,
                                                           "contact_person":contact_name,
                                                           "contact_number":contact_number,
                                                           "contact_email":email}]), ttl='0')
            st.rerun()
        else:
            st.write("Please fill all required fields")
