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

engineers = list(pd.DataFrame(execute_query(conn.table("Engineers").select("name", count="None"), ttl=None).data)["name"])
df = execute_query(conn.table("Logs").select("*", count="None"), ttl="0")

if len(df.data) > 0:
        df = pd.DataFrame(df.data)[["id", "created_at", "location", "priority", "problem", "engineer", "image", "completed", "completed_at", "call_report"]]

        event =st.dataframe(df, use_container_width=True, hide_index=True, height=400, 
                on_select="rerun",
                selection_mode="single-row",column_config={
                        "id":"ID",
                        "created_at":st.column_config.DatetimeColumn("Created At"),
                        "location":"Company - Branch",
                        "priority":"Priority",
                        "problem":"Problem Statement",
                        "engineer":"Engineer Name",
                        "image":st.column_config.ListColumn("Images"),
                        "completed":st.column_config.CheckboxColumn("Completed"),
                        "completed_at":st.column_config.DatetimeColumn("Completed At"),
                        "call_report":st.column_config.ListColumn("Call Reports"),
                })

        if event.selection.rows:
                selected_row = df.iloc[event.selection.rows].copy().reset_index()
                id = selected_row["id"][0]
                created_at = selected_row["created_at"][0]
                location = selected_row["location"][0]
                priority = selected_row["priority"][0]
                problem = selected_row["problem"][0]
                engineer = selected_row["engineer"][0]
                images = selected_row["image"][0]
                completed = selected_row["completed"][0]
                completed_at = selected_row["completed_at"][0]
                call_report = selected_row["call_report"][0]

                with st.form("Edit"):

                        st.title(location)
                        st.write(datetime.strptime(created_at[0:19], "%Y-%m-%dT%H:%M:%S")+timedelta(hours=5, minutes=30))
                        st.write(id)

                        priorityInput = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(priority))

                        problemInput = st.text_area("Problem Statement", value=problem)
                        engineerInput = st.selectbox("Engineer", options=engineers, index=engineers.index(engineer))

                        placeholderImage1 = st.empty()
                        placeholderImage2 = st.empty()
                        placeholderImage3 = st.empty()

                        completedInput = st.toggle("Completed", completed)
                        col1Completed, col2Completed = st.columns([1,1])
                        with col1Completed:
                                completedDate = st.date_input("Completed At")
                        with col2Completed:
                                completedTime = st.time_input("Completed At")


                        placeholderCallReport1 = st.empty()
                        placeholderCallReport2 = st.empty()
                        placeholderCallReport3 = st.empty()

                        col1Bottom, col2Bottom = st.columns([1,1])
                        with col1Bottom:
                                delete = st.form_submit_button("Delete Ticket", type="primary", use_container_width=True)
                        with col2Bottom:
                                save = st.form_submit_button("Save Changes", use_container_width=True)
                
                with placeholderImage1:
                        newImageInput = st.file_uploader(label="Images", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True)
                with placeholderImage2:
                        imageInput = st.multiselect("Images", images+newImageInput, images+newImageInput)
                with placeholderImage3:
                        if imageInput != None:
                                with st.container():
                                        for i in imageInput:
                                                if isinstance(i, str):
                                                        data = conn.download("images" ,source_path=i, ttl=None)
                                                        st.image(data[0])
                                                else:
                                                        st.image(i)
                with placeholderCallReport1:
                        newCallReportInput = st.file_uploader(label="Call Reports", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True)
                with placeholderCallReport2:
                        callReportInput = st.multiselect("Call Reports", call_report+newCallReportInput, call_report+newCallReportInput)
                with placeholderCallReport3:
                        if callReportInput != None:
                                with st.container():
                                        for i in callReportInput:
                                                if isinstance(i, str):
                                                        data = conn.download("images" ,source_path=i, ttl=None)
                                                        st.image(data[0])
                                                else:
                                                        st.image(i)

                if save:
                        for i in imageInput:
                                if not isinstance(i, str):
                                        filename = "images/"+str(datetime.now())+i.__getattribute__("name")
                                        conn.upload("images", "local",i , filename)
                                        imageInput.append(filename)
                                        imageInput.remove(i)
                        for i in callReportInput:
                                if not isinstance(i, str):
                                        filename = "call_reports/"+str(datetime.now())+i.__getattribute__("name")
                                        conn.upload("images", "local",i , filename)
                                        callReportInput.append(filename)
                                        callReportInput.remove(i)
                
                        execute_query(conn.table('Logs').update([{
                                "priority":priorityInput,
                                "problem":problemInput,
                                "engineer":engineerInput,
                                "image":imageInput,
                                "completed":str(completedInput),
                                "completed_at":str(datetime.combine(completedDate, completedTime)),
                                "call_report":callReportInput,
                        }]).eq("id", id), ttl='0')
                        st.rerun()
                
                if delete:
                        execute_query(conn.table('Logs').delete(count=None).eq("id", id), ttl='0')
                        st.rerun()

else:
        st.write("No Records")      

