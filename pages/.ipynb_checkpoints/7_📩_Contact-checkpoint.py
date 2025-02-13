
import streamlit as st

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

contact_col1, contact_col2= st.columns(2)
with contact_col1:
    contact_col1.markdown("<h4 style='background-color: #0033A0; text-align: center; color: 	white;'>Mohammad Shamim</h2>", unsafe_allow_html=True)
    contact_form = """
    <form action="https://formsubmit.co/shamim.one@outlook.com" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder = "Your Name"required>
    <input type="email" name="email" placeholder = "Email Address" required>
    <textarea name="message" placeholder="Your message here"></textarea>
    <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html = True)
    def local_css(file_name):
        with open(file_name) as f:
            contact_col1.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    local_css("style.css")



with contact_col2:
    contact_col2.markdown("<h4 style='background-color: #0033A0; text-align: center; color: 	white;'>Robbie Williams</h2>", unsafe_allow_html=True)
    contact_form = """
    <form action="https://formsubmit.co/rwilliamsfarms@bellsouth.net" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder = "Your Name"required>
    <input type="email" name="email" placeholder = "Email Address" required>
    <textarea name="message" placeholder="Your message here"></textarea>
    <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html = True)
    def local_css(file_name):
        with open(file_name) as f:
            contact_col2.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    local_css("style.css")