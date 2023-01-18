# import libraries
import streamlit as st
import matplotlib.pyplot as plt

# configure the page
st.set_page_config(
    page_title="Lime Calculator with Charts",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="expanded"
)

# This is a CSS styling that affects some part of the App.
st.markdown(
    """
<style>
.reportview-container .markdown-text-container {
    font-family: monospace;
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: light blue;
}

[class^="st-b"] {
    color: black;
    font-size = 25px;
    font-weight= bold;
    color: black;
    font-family: monospace;
}

</style>
""",
    unsafe_allow_html=True,
)


# Lets add a title to our App 
# add some information

st.markdown("<h1 style='background-color: #0033A0; text-align: center; color: 	white;'>Lime Calculator with Color Charts</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='background-color: #0033A0;text-align: center; color: 	white;'>Particle Analysis, CCE, RNV, pH, Buffer pH, Rates, and Cost/Acre</h4>", unsafe_allow_html=True)
st.markdown(
"""<div style="text-align: justify;">
All rights reserved. </br>
<span style = "color: red;"> Disclaimer: </span>This open source web application was developed by <a href = 'https://www.linkedin.com/in/mohammad-jan-shamim-693136112/'>Mohammad Shamim</a> and Robbie Williams in Henderson, Kentucky, USA.</br>
It comes with absolutely no warranty and the authors accept no liability. You are welcome to distribute it for scientific uses following the authors' consent.</br>
You can perform calculations either by manually inserting values into cells in the "Calculator Manual" menu or by uploading the values in a CSV file in the "Calculator CSV" menu. 
The manual form allows up to five lime sources calculations. 
Uploading a CSV file allows an unlimited number of lime sources calculations. You can choose your favorite color for the charts from over 100 color palettes in the "Setting" menu.</br>
Be sure to check boxes/toggle buttons for desired calculations. 
This web app uses Sikora-2 buffer for determining the quantity and cost of lime to be applied in an acre. </br>
We are greatly indebted to <a href =' https://pss.ca.uky.edu/person/frank-sikora'>Dr. Frank Sikora</a>, 
Regulatory Services, the University of Kentucky, USA, for his invaluable input in this Web App. </br>
Should you have any quesions and suggestions, please do not hesitate to contact us. </br>
</br>
<span style = 'color:blue; font-weight: bold'>Read more...</span>
</br>
    <a href = 'http://www2.ca.uky.edu/agcomm/pubs/id/id163/id163.pdf'> Agricultural Lime Recommendation Based on Lime Quality </a> </br>
    <a href = "https://www.rs.uky.edu/soil/technical_info/">Rock Quarry Lime Reports - University of Kentucky</a>
</div>
    """, unsafe_allow_html=True)

st.write("")
image1, image2 = st.columns(2)
img1 = plt.imread('Lime particles .jpg')
img2 = plt.imread('Sieves1.jpg')
image1.image(img2)
image2.image(img1)
st.caption("Photo Credit: Robbie Williams")