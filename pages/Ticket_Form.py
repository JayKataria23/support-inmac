import streamlit as st
import datetime
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query


st.set_page_config(page_title='Support Ticket Workflow', page_icon="https://inmac.co.in/wp-content/uploads/2023/08/cropped-ms-icon-310x310-1-32x32.png")
st.image("https://inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png")
conn = st.connection("supabase",type=SupabaseConnection)
tId = str(int(execute_query(conn.table("Logs").select("id", count="Exact").order('id', desc=True)
    .limit(1)
, ttl=None).data[0]["id"][1:])+1)
st.title( 'Write a ticket: '+tId)

locations = list(pd.DataFrame(execute_query(conn.table("Locations").select("name", count="None"), ttl=None).data)["name"])
engineers = list(pd.DataFrame(execute_query(conn.table("Engineers").select("name", count="None"), ttl=None).data)["name"])

with st.form('ticket', clear_on_submit=True):
    location = st.selectbox("Company - Branch*", locations,  index=None)
    issue = st.text_area('Description of issue')
    serialNumbers = st.text_area('Serial Number\'s', placeholder="Seperate with comma")
    priority = st.selectbox('Priority', ['High', 'Medium', 'Low'], index=2)
    image = st.file_uploader("Add Image", accept_multiple_files=True, type=['png', 'jpg', 'webp', 'jpeg'])
    engineer = st.selectbox("Engineer", engineers, index=None)
    submit = st.form_submit_button('Submit')


    if submit:
        if location != "" and issue != "" and priority != "":
            serialNumbers = serialNumbers.replace(" ", "").split(",")
            images = []
            if image is not None:
                for i in image:
                    filename = "images/"+str(datetime.datetime.now())+i.__getattribute__("name")
                    conn.upload("images", "local",i , filename)
                    images.append(filename)
                    st.write(i.__getattribute__("name").split('.')[-1])
            

            execute_query(conn.table('Logs').insert([{
                "location":location,
                "problem":issue,
                "engineer":engineer,
                "image":images,
                "serialNumbers":serialNumbers,
                "activeTime":[str(datetime.datetime.now())],
                "priority":priority,
                "pause":False
            }]), ttl='0')
            st.rerun()
        else:
            st.write("Please fill all required fields")
