import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query


conn = st.connection("supabase",type=SupabaseConnection)

st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Update Engineer')

engineers = list(pd.DataFrame(execute_query(conn.table("Engineers").select("name", count="None"), ttl=None).data)["name"])

engineerInput = st.selectbox("Engineer", options=engineers, index=None)
if engineerInput is not "" and engineerInput is not None:
    data = execute_query(conn.table("Engineers").select("*", count="None").eq('name', engineerInput), ttl=None).data[0]
    st.write(data)
    with st.form('engineer'):
        number = st.text_input('Phone Number*', value=data["contact_number"])
        email = st.text_input('Email ID*', value=data["email"])
        field = st.toggle("Field Engineer", value=data["field"])
        location = st.text_input('Location', value=data["location"])
        placeholder_for_selectbox = st.empty()
        placeholder_for_optional_text = st.empty()
        submit = st.form_submit_button('Submit')


    with placeholder_for_selectbox:
        if data["domain"] in ["Hardware Engineer", "PM Engineer", "Printer Engineer", "Other"]:
            selection = st.selectbox("Domain", ["Hardware Engineer", "PM Engineer", "Printer Engineer", "Other"], index=0)
        else:
            selection = "Other"
        
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
                    "domain":domain
                    }]), ttl='0')
                st.rerun()
            else:
                st.write("Please fill all required fields")
