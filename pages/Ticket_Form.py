import streamlit as st
import datetime
from st_supabase_connection import SupabaseConnection, execute_query


conn = st.connection("supabase",type=SupabaseConnection)

st.image("https://i0.wp.com/inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png?w=721&ssl=1")
st.title( 'Write a ticket')

with st.form('ticket'):
    location = st.selectbox("Company - Branch*", ["TJSB bank - Yewatamal","TJSB bank - Solapur","TJSB bank - Akola",],  index=None)
    issue = st.text_area('Description of issue')
    priority = st.selectbox('Priority', ['High', 'Medium', 'Low'], index=2)
    image = st.file_uploader("Add Image", accept_multiple_files=True, type=['png', 'jpg', 'webp', 'jpeg'])
    engineer = st.selectbox("Engineer", ["Irshad Sidique", "Shafiq Khan", "Ravi Patil", "Arun Nikade"], index=None)
    submit = st.form_submit_button('Submit')


    if submit:
        if location != "" and issue != "" and priority != "":
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
                "priority":priority
            }]), ttl='0')
            st.rerun()
        else:
            st.write("Please fill all required fields")