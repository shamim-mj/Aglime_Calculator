# Import libraries
import pandas as pd
import streamlit as st
import datetime
from st_aggrid import AgGrid
import matplotlib.pyplot as plt

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

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
radio = col2.radio("Which data do you want to download", options = ['Manually input data', 'From uploaded file', 'Ohio State Data'], label_visibility='collapsed')

# check what the user asked for
if radio == 'Manually input data':
    if "df" not in st.session_state:
        st.write("**:red[No data to download!]**")    
    else:
        df = st.session_state['df']
        df = round(df, 2)
        AgGrid(df.loc[:, ['Quarry', 'Zero%_eff', 'Fifty%_eff', 'Hund%_eff', "RNV", 'Bulk_Rec', 'Cost']], columns_auto_size_mode='FIT_ALL_COLUMNS_TO_VIEW', theme='alpine')
        st.caption("**:blue[This dataframe is interactive. You can scroll left-to-right, top-to-bottom, freez columns, and filter them. Please download the file before navigating to another menu. You will lose the data otherwise!]**")
        cbox = st.checkbox('Descriptions')
        if cbox:
            st.markdown("""
            <div style ='text-aling: justify;'>
            ??? Zero%_eff:           Percent me that is not effective </br>
            ??? Fifty%_eff:          Percent lime  that is 50 percent effecitve </br>
            ??? Hund%_eff:           Percent lime that is  100 percent effetive </br>
            ??? RNV:                 Relative Neutralizing Value </br>
            ??? Bulk_Rec:            Amount of lime recommended to be applied in an acre to raise soil pH to a target pH </br>
            ??? Cost:                Application cost per acre
            </div>
            """, unsafe_allow_html = True)

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
        AgGrid(df.loc[:, ['Quarry', 'Zero%_eff', 'Fifty%_eff', 'Hund%_eff', "RNV", 'Bulk_Rec', 'Cost']], columns_auto_size_mode='FIT_ALL_COLUMNS_TO_VIEW', theme='alpine')
        st.session_state['downloaded_data'] = df
        st.caption("**:blue[This dataframe is interactive. You can scroll left-to-right, top-to-bottom, freez columns, and filter them. Please download the file before navigating to another menu. You will lose the data otherwise!]**")
        cbox = st.checkbox('Descriptions')
        if cbox:
            st.markdown("""
            <div style ='text-aling: justify;'>
            ??? Zero%_eff:           Percent me that is not effective </br>
            ??? Fifty%_eff:          Percent lime  that is 50 percent effecitve </br>
            ??? Hund%_eff:           Percent lime that is  100 percent effetive </br>
            ??? RNV:                 Relative Neutralizing Value </br>
            ??? Bulk_Rec:            Amount of lime recommended to be applied in an acre to raise soil pH to a target pH </br>
            ??? Cost:                Application cost per acre
            </div>
            """, unsafe_allow_html = True)
elif radio == "Ohio State Data":
    if "df_oh" not in st.session_state:
        st.write("**:red[You  have not done any calculations using Ohio State Method]**")
    else:
        df = st.session_state['df_oh']
        df = round(df,2)
        AgGrid(round(df.loc[:,['Quarry','FI', "%_ENP", "t_ENP", "Bulk_Rec", "Cost"]], 2),  columns_auto_size_mode='FIT_ALL_COLUMNS_TO_VIEW', theme='alpine')
        cbox = st.checkbox('Descriptions')
        if cbox:
            st.markdown("""
            <div style ='text-aling: justify;'>
            ??? FI:          Fineness Index (%) </br>
            ??? %_ENP:       Effective Neutralizing Power (%) </br>
            ??? t_ENP:       The amount of total neutralizing power in a ton </br>
            ??? Bulk_Rec:    The amount of lime to applied in an acre </br>
            ??? Cost:        Total cost (lime, delivery, and spreading)
            </div>
            """, unsafe_allow_html = True)
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
st.markdown('___')



st.markdown("<h3 style=' text-align: center; background-color: #0033A0;  color: white;'>Excel Version of the Calculator</h3>", unsafe_allow_html=True)
st.markdown("<h4 style=' text-align: center; background-color: white;  color: black;'>""</h4>", unsafe_allow_html=True)

st.markdown("<a href='https://github.com/shamim-mj/Aglime_Calculator_in_Excel.git'> Click to download an Excel version of the Calculator!</a>", unsafe_allow_html = True)

with st.expander("**Read Instruction**"):
    st.write("The link will take you to our github webpage where the following window will appear")
    img1 = plt.imread('Excel1.jpg')
    st.image(img1)
    st.write("Clicking on 'Lime Calculator Excel.xlsx' will open the follwing window")
    img2 = plt.imread('Excel2.jpg')
    st.image(img2)
    st.write("Click the download button. Woohoo, the file will  start downloading")
    