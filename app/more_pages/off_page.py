import os
import sys
import streamlit as st
import pandas as pd
import logging
import re
from io import StringIO
from pydantic.tools import parse_obj_as
from st_pages import add_indentation

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(CURRENT_DIR))

from app.const import OFF_TARGET_TEXT_HELP
from app.object_def import OffTargetList
from app.utills import load_data, get_server_db_info
from app.general_info import process_data

st.set_page_config(layout="wide", page_title="OffRisk v.1.0")

add_indentation()

log = logging.getLogger("off-risk-ui-log")



hide_streamlit_style = """
    <style>
    footer {visibility: hidden; padding:0}
"""

# Hide streamlit style (footer)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title('Off-targets input page')
st.header('Please choose server and databases for off-target analysis')
get_server_db_info()
st.markdown("---")

col1, col2 = st.columns((1, 1))
col1.write('Upload tsv file for off-target analysis')
off_target_uploaded_file = col1.file_uploader("Off-Target file upload", type=[".tsv"], help=OFF_TARGET_TEXT_HELP)

col2.write('Fill the following for off-target analysis')
off_target_data = col2.text_area("Off-Target text", height=117, help=OFF_TARGET_TEXT_HELP)
st.markdown("---")

if st.button("Run"):
    if not off_target_uploaded_file and not off_target_data:
        st.error("Please upload a file or insert data to for analysis")
    else:
        tmp_df = pd.DataFrame()
        if off_target_uploaded_file:
            log.info("Loading the data from {}".format(off_target_uploaded_file))
            # Validate file name input
            val_user_input_file = re.match(r"[A-Za-z0-9_\-\\]+\.tsv", off_target_uploaded_file.name)
            if val_user_input_file and val_user_input_file.group() == off_target_uploaded_file.name:
                # Create request body
                tmp_df = pd.read_csv(StringIO(off_target_uploaded_file.getvalue().decode("utf-8")),
                                     sep="\t", header=None)
            else:
                st.error("File name is not in the correct format. File must be tsv type, "
                         "and contain only letters and numbers")
        elif off_target_data:
            off_target_data = off_target_data.replace(" ", "\t") #should we not replace with \s+?
            tmp_df = pd.read_csv(StringIO(off_target_data), sep="\t", header=None)

        if not tmp_df.empty:
            tmp_df.rename(columns={0: "chromosome", 1: "start", 2: "end", 3: "strand"}, inplace=True)
            # Validate input
            request_body = parse_obj_as(OffTargetList, {"off_targets": tmp_df.to_dict("records")}).dict()
            # Create request body
            request_body["db_list"] = st.session_state.dbs
            all_result = load_data(2, request_body, st.session_state.server_url)
            if all_result:
                process_data(all_result)

        else:
            pass
