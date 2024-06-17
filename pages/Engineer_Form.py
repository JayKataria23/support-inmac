import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query


conn = st.connection("supabase",type=SupabaseConnection)

st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Add Engineer to DB')

with st.form('engineer'):
    name = st.text_input('Name*', )
    number = st.text_input('Phone Number*')
    email = st.text_input('Email ID*')
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
                                                          "domain":domain}]), ttl='0')
            st.rerun()
        else:
            st.write("Please fill all required fields")