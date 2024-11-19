import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query


st.set_page_config(page_title='Support Ticket Workflow', page_icon="https://inmac.co.in/wp-content/uploads/2023/08/cropped-ms-icon-310x310-1-32x32.png")
st.image("https://inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png")
st.title( 'Update Location')

conn = st.connection("supabase",type=SupabaseConnection)

locations = list(pd.DataFrame(execute_query(conn.table("Locations").select("name", count="7980"), ttl=None).data)["name"])
locationInput = st.selectbox("Company - Branch", options=locations, index=None)
if locationInput is not "" and locationInput is not None:
    data = execute_query(conn.table("Locations").select("*", count="None").eq('name', locationInput), ttl=None).data[0]
    with st.form('locations'):
        address = st.text_area('Address*', value=data["address"])
        pincode = st.text_input('Pincode', value=data["pincode"])
        contactPerson = st.text_input('Contact Person', value=data["contact_person"])
        contactNumber = st.text_input('Contact Number', value=data["contact_number"])
        contactEmail = st.text_input('Contact Email', value=data["contact_email"])

        col1Bottom, col2Bottom = st.columns([1,1])
        with col1Bottom:
                delete = st.form_submit_button("Remove Location", type="primary", use_container_width=True)
        with col2Bottom:
                save = st.form_submit_button("Save Changes", use_container_width=True)



        if save:
            execute_query(conn.table('Locations').update([{
                "address":address,
                "pincode":pincode,
                "contact_number":contactNumber,
                "contact_person":contactPerson,
                "contact_email":contactEmail,
                }]).eq('name', locationInput), ttl='0')
            st.rerun()
        
        if delete:
            execute_query(conn.table('Locations').delete(count=None).eq('name', locationInput), ttl='0')
            st.rerun()
    

