# Import libraries
import pandas as pd
import streamlit as st
import datetime
from st_aggrid import AgGrid

# give it a name
st.markdown("<h2 style='background-color: #0033A0; font-size:35px; text-align: center; color: 	white;'>Output File</h2>", unsafe_allow_html=True)
st.markdown("<h3 style=' text-align: center; color: black;'>""</h3>", unsafe_allow_html=True)

# create a date and include it togather with time so that each file is unique and traceable
date1, _,_,_,_ = st.columns(5)
date1.markdown("<h5 style=' background-color: #0033A0; text-align: center; color: white;'>Date</h5>", unsafe_allow_html=True)
date = date1.date_input("date", label_visibility='collapsed')
time = datetime.datetime.now().time()

# Since we have manual and uploaded data, here giving the user choice of downloading data
st.markdown("<h3 style=' text-align: center; color: black;'>Which data do you want to download</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
radio = col2.radio("Which data do you want to download", options = ['Manually input data', 'From uploaded file'], label_visibility='collapsed')

# check what the user asked for
if radio == 'Manually input data':
    if "df" not in st.session_state:
        st.write("**:red[No data to download!]**")    
    else:
        df = st.session_state['df']
        df = round(df, 2)
        AgGrid(df, columns_auto_size_mode=True, )
        st.caption("**:blue[This dataframe is interactive. You can scroll left-to-right, top-to-bottom, freez columns, and filter them. Please download the file before navigating to another manu. You will lose the data otherwise!]**")

        # Preparing data to download
        df1 = df.to_csv().encode('utf-8')
        # this checkbox will allow us to download data
        st.markdown("### **:blue[Download!]**")
        st.download_button(
            key = 'b_csv',
            label = "Download data as csv file",
            data = df1,
            file_name = f"Lime_particle_analysis_[{date}]_[{time}].csv",
            mime = 'text/csv'
        )
        st.caption(":red[Note that a default dataset, corresponding to the number of open slots, is downloaded if you don't insert values in the form or don't upload  a file]")
elif radio == 'From uploaded file':
    if "df_up" not in st.session_state:
        st.write("**:red[You have not uploaded data!]**")
    else:
        df = st.session_state['df_up']
        df = round(df, 2)
        # st.dataframe((df.set_index('Quarry').style.format("{:.2f}")))
        AgGrid(df, columns_auto_size_mode=True )
        st.session_state['downloaded_data'] = df
        st.caption("**:blue[This dataframe is interactive. You can scroll left-to-right, top-to-bottom, freez columns, and filter them. Please download the file before navigating to another manu. You will lose the data otherwise!]**")

        # Preparing data to download
        df1 = df.to_csv().encode('utf-8')

        st.markdown("### **:blue[Download!]**")
        st.download_button(
            key = 'b_csv',
            label = "Download data as csv file",
            data = df1,
            file_name = f"Lime_particle_analysis_[{date}]_[{time}].csv",
            mime = 'text/csv'
        )
        st.caption(":red[Note that a default dataset, corresponding to the number of open slots, is downloaded if you don't insert values in the form or don't upload  a file]")
        