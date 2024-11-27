import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from st_supabase_connection import SupabaseConnection, execute_query

# Page title

st.set_page_config(page_title='Support Ticket Workflow', page_icon="https://inmac.co.in/wp-content/uploads/2023/08/cropped-ms-icon-310x310-1-32x32.png")
st.image("https://inmac.co.in/wp-content/uploads/2022/09/INMAC-web-logo.png")
st.title( 'Support Ticket Workflow')

conn = st.connection("supabase",type=SupabaseConnection)

engineers = list(pd.DataFrame(execute_query(conn.table("Engineers").select("name", count="None"), ttl=None).data)["name"])
df = execute_query(conn.table("Logs").select("*", count="None"), ttl="0")

if len(df.data) > 0:
        df = pd.DataFrame(df.data)[["id", "created_at", "location", "priority", "problem", "engineer", "image", "completed", "completed_at", "call_report", "serialNumbers", "activeTime", "pause"]]
        df = df.sort_values(by='id', ascending=False)
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
                        "serialNumbers":st.column_config.ListColumn("Serial Numbers"), 
                        "activeTime":st.column_config.ListColumn("Active Time"), 
                        "pause":"Paused"

                })

        if event.selection.rows:
                selected_row = df.iloc[event.selection.rows].copy().reset_index()
                id = selected_row["id"][0]
                created_at = selected_row["created_at"][0]
                location = selected_row["location"][0]
                priority = selected_row["priority"][0]
                problem = selected_row["problem"][0]
                serialNumbers = ",".join(selected_row["serialNumbers"][0])
                engineer = selected_row["engineer"][0]
                images = selected_row["image"][0]
                completed = selected_row["completed"][0]
                completed_at = selected_row["completed_at"][0]
                call_report = selected_row["call_report"][0]
                activeTime = selected_row["activeTime"][0]
                paused = selected_row["pause"][0]

                with st.form("Edit"):

                        st.title(location)
                        st.write(datetime.strptime(created_at[0:19], "%Y-%m-%dT%H:%M:%S")+timedelta(hours=5, minutes=30))
                        st.write(id)

                        priorityInput = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(priority))

                        problemInput = st.text_area("Problem Statement", value=problem)
                        serialNumbers = st.text_area('Serial Number\'s', placeholder="Seperate with comma", value=serialNumbers)
                        engineerInput = st.selectbox("Engineer", options=engineers, index=engineers.index(engineer))

                        pausedInput = st.toggle("Pause", paused)

                        placeholderImage1 = st.empty()
                        placeholderImage2 = st.empty()
                        placeholderImage3 = st.empty()

                        placeholderCompletedAt = st.empty()
                        col1Completed, col2Completed = st.columns([1,1])
                        with col1Completed:
                                placeholderCompletedAt1 = st.empty() 
                        with col2Completed:
                                placeholderCompletedAt2 = st.empty() 


                        placeholderCallReport1 = st.empty()
                        placeholderCallReport2 = st.empty()
                        placeholderCallReport3 = st.empty()

                        col1Bottom, col2Bottom = st.columns([1,1])
                        with col1Bottom:
                                delete = st.form_submit_button("Delete Ticket", type="primary", use_container_width=True)
                        with col2Bottom:
                                save = st.form_submit_button("Save Changes", use_container_width=True)
                if len(call_report)==1:
                        file_name, mime, data = conn.download("images" ,source_path=call_report[0], ttl=None)
                        dnld_btn = st.download_button("Download Call Report", data = data, file_name=file_name+".jpg", mime = mime)
                with placeholderCompletedAt:
                        completedInput = st.toggle("Completed", completed)

                if completedInput == True:
                        if completed==False:
                                with placeholderCompletedAt1:    
                                        completedDate = st.date_input("Completed At", value = None)
                                with placeholderCompletedAt2:
                                        completedTime = st.time_input("Completed At", value = None)
                        else:
                                with placeholderCompletedAt1:    
                                        completedDate = st.date_input("Completed At", value = datetime.strptime(completed_at[0:10], "%Y-%m-%d"))
                                with placeholderCompletedAt2:
                                        completedTime = st.time_input("Completed At", value = datetime.strptime(completed_at[12:20], "%H:%M:%S"))



                with placeholderImage1:
                        newImageInput = st.file_uploader(label="Images", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True)
                        if newImageInput is None:
                                newImageInput = []
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
                        if newCallReportInput is None:
                                newCallReportInput = []
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
                        serialNumbers = serialNumbers.replace(" ", "").split(",")
                        for i in imageInput:
                                if not isinstance(i, str):
                                        filename = "images/"+str(datetime.now())+"Ticket_"+id
                                        conn.upload("images", "local",i , filename)
                                        imageInput.append(filename)
                                        imageInput.remove(i)
                        for i in callReportInput:
                                if not isinstance(i, str):
                                        filename = "call_reports/"+str(datetime.now())+"Ticket_"+id
                                        conn.upload("images", "local",i , filename)
                                        callReportInput.append(filename)
                                        callReportInput.remove(i)
                        if completedInput:
                                completed_at = str(datetime.combine(completedDate, completedTime))
                        else:
                                completed_at=None

                        if paused != pausedInput:
                                activeTime.append(str(datetime.now()))

                        
                        execute_query(conn.table('Logs').update([{
                                "priority":priorityInput,
                                "problem":problemInput,
                                "serialNumbers":serialNumbers,
                                "engineer":engineerInput,
                                "image":imageInput,
                                "completed":str(completedInput),
                                "completed_at": completed_at,
                                "call_report":callReportInput,
                                "activeTime":activeTime,
                                "pause":pausedInput
                        }]).eq("id", id), ttl='0')
                        st.rerun()
                
                if delete:
                        execute_query(conn.table('Logs').delete(count=None).eq("id", id), ttl='0')
                        st.rerun()

else:
        st.write("No Records")      

