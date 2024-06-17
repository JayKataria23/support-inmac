import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query


conn = st.connection("supabase",type=SupabaseConnection)

st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Add Engineer to DB')

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