import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query



st.set_page_config(page_title='Support Ticket Workflow', page_icon="https://inmac.co.in/wp-content/uploads/2023/08/cropped-ms-icon-310x310-1-32x32.png")
st.image("https://inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png")
st.title( 'Update Engineer')

conn = st.connection("supabase",type=SupabaseConnection)

engineers = list(pd.DataFrame(execute_query(conn.table("Engineers").select("name", count="None"), ttl=None).data)["name"])

engineerInput = st.selectbox("Engineer", options=engineers, index=None)
if engineerInput is not "" and engineerInput is not None:
    data = execute_query(conn.table("Engineers").select("*", count="None").eq('name', engineerInput), ttl=None).data[0]
    with st.form('engineer'):
        number = st.text_input('Phone Number*', value=data["contact_number"])
        email = st.text_input('Email ID*', value=data["email"])
        field = st.toggle("Field Engineer", value=data["field"])
        location = st.text_input('Location', value=data["location"])
        placeholder_for_selectbox = st.empty()
        placeholder_for_optional_text = st.empty()

        col1Bottom, col2Bottom = st.columns([1,1])
        with col1Bottom:
                delete = st.form_submit_button("Remove Engineer", type="primary", use_container_width=True)
        with col2Bottom:
                save = st.form_submit_button("Save Changes", use_container_width=True)


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

        if save:
            if number != "" and email != "" and domain != "":
                execute_query(conn.table('Engineers').update([{
                    "contact_number":number,
                    "email":email,
                    "field":field,
                    "location":location,
                    "domain":domain
                    }]).eq('name', engineerInput), ttl='0')
                st.rerun()
            else:
                st.write("Please fill all required fields")
        
        if delete:
            execute_query(conn.table('Engineers').delete(count=None).eq('name', engineerInput), ttl='0')
            st.rerun()
    

