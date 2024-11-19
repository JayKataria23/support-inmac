import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query




st.set_page_config(page_title='Support Ticket Workflow', page_icon="https://inmac.co.in/wp-content/uploads/2023/08/cropped-ms-icon-310x310-1-32x32.png")
st.image("https://inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png")
st.title( 'Add Engineer to DB')

conn = st.connection("supabase",type=SupabaseConnection)

with st.form('engineer'):
    name = st.text_input('Name*', )
    number = st.text_input('Phone Number*')
    email = st.text_input('Email ID*')
    field = st.toggle("Field Engineer")
    location = st.text_input('Location')
    placeholder_for_selectbox = st.empty()
    placeholder_for_optional_text = st.empty()
    submit = st.form_submit_button('Submit')


with placeholder_for_selectbox:
    selection = st.selectbox("Domain", ["Hardware Engineer", "PM Engineer", "Printer Engineer", "Other"], index=0)
    
with placeholder_for_optional_text:
    if selection == "Other":
        domain = st.text_input("If other, Specify")
    else:
        domain = selection

    if submit:
        if name != "" and number != "" and email != "" and domain != "":
            st.write(number+name+email+domain)
            execute_query(conn.table('Engineers').insert([{
                                                            "contact_number":number,
                                                            "name":name,
                                                            "email":email,
                                                            "field":field,
                                                            "location":location,
                                                            "domain":domain}]), ttl='0')
            st.rerun()
        else:
            st.write("Please fill all required fields")
