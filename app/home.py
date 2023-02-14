import logging
import streamlit as st
import pandas as pd

from utills import init_logger

st.set_page_config(layout="wide", page_title="OffRisk v.1.0")

# Main
hide_streamlit_style = """
    <style>
    footer {visibility: hidden; padding:0}
"""

# Hide streamlit style (footer)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Init logging
init_logger(logger_name="off-risk-ui-log")
log = logging.getLogger("off-risk-ui-log")

# global
if "off_target" not in st.session_state:
    st.session_state['off_target'] = pd.DataFrame()

if "flashfry_score" not in st.session_state:
    st.session_state["flashfry_score"] = pd.DataFrame()

# Sidebar Options
all_result = None


st.title('Welcome to OffRisk !')
st.write('''OffRisk Data Explorer is a tool designed using Python and Streamlit to help you view and 
gain an understanding of the contents of your off / on target samples.''')
st.write('To begin using the app, if you wish for off-target, load your TSV file using the file upload '
         'option on the sidebar, if you wish for on'
         '-target, paste your input to the text box at the slide bar.'
         ' Once you have done this, '
         ' you can navigate to the relevant tools using the Navigation menu.')
