import json
import logging
import os
import re
import sys
from io import StringIO

from typing import List
import streamlit as st
from pydantic.tools import parse_obj_as
from st_pages import add_indentation

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(CURRENT_DIR))

from app.const import ON_TARGET_UPLOAD_HELP, TOOLS_NAME_LIST
from app.general_info import process_data
from app.object_def import Site, SitesList
from app.utills import load_data, get_server_db_info

st.set_page_config(layout="wide", page_title="OffRisk v.1.0")

log = logging.getLogger("off-risk-ui-log")

add_indentation()

if "pam" not in st.session_state:
    st.session_state.pam = "NGG"

if "tools" not in st.session_state:
    st.session_state.tools = [list(TOOLS_NAME_LIST.keys())[0]]

if "dna_bulge" not in st.session_state:
    st.session_state.dna_bulge = 0

if "rna_bulge" not in st.session_state:
    st.session_state.rna_bulge = 0

if "pam_location" not in st.session_state:
    st.session_state.pam_location = "Downstream"

if "sequence" not in st.session_state:
    st.session_state.sequence = ""

if "mismatch" not in st.session_state:
    st.session_state.mismatch = 0

if "flashfry" in st.session_state.tools:
    st.session_state.pam = "NGG"
    st.session_state.pam_location = "Downstream"
    st.session_state.dna_bulge = 0
    st.session_state.rna_bulge = 0

hide_streamlit_style = """
    <style>
    footer {visibility: hidden; padding:0}
"""

# Hide streamlit style (footer)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title('gRNA input page')
st.header('Please choose server and databases for on-target analysis')
get_server_db_info()
st.markdown("---")

st.header('Off-target search tool')
tools_selection = st.multiselect("Please select off-target search tool", list(TOOLS_NAME_LIST.keys()),
                                 format_func=lambda v: TOOLS_NAME_LIST[v], key='tools')

st.markdown("---")

st.header('Fill the following for on target analysis. Sequence is a mandatory field')
col1, col2, col3, col4 = st.columns((3, 1, 0.5, 0.5))
col1.text_input("Protospacer Adjacent Motif (PAM)", max_chars=50, key="pam",
                             disabled="flashfry" in st.session_state.tools)
col2.selectbox("Location", ("Downstream", "Upstream"), key="pam_location",
                          disabled="flashfry" in st.session_state.tools)
col3.number_input("DNA bulge", min_value=0, max_value=len(st.session_state.sequence), key="dna_bulge",
                            disabled="flashfry" in st.session_state.tools or len(st.session_state.sequence) == 0)
col4.number_input("RNA bulge", min_value=0, max_value=len(st.session_state.sequence), key="rna_bulge",
                            disabled="flashfry" in st.session_state.tools or len(st.session_state.sequence) == 0)

col1, col2 = st.columns((3, 1))
col1.text_input("Sequence",
                # min_chars=20 if "flashfry" in st.session_state.tools else 0,
                max_chars=20 if "flashfry" in st.session_state.tools else 50, key="sequence")
col2.number_input("Mismatch", min_value=0, max_value=len(st.session_state.sequence),
                  disabled=len(st.session_state.sequence) == 0, key="mismatch")

st.markdown("---")

st.header('Upload json file for on-target analysis')
on_target_uploaded_file = st.file_uploader("On-Target file upload", type=[".json"], help=ON_TARGET_UPLOAD_HELP)
st.markdown("---")



if st.button("Run"):
    if not on_target_uploaded_file and not st.session_state.sequence:
        st.error("Please upload a file or insert data to for analysis")
    else:
        # file input
        if on_target_uploaded_file:
            log.info("Loading the data from {}".format(on_target_uploaded_file))
            # Validate file name input
            val_user_input_file = re.match(r"[A-Za-z0-9_\-\\]+\.json", on_target_uploaded_file.name)
            if val_user_input_file and val_user_input_file.group() == on_target_uploaded_file.name:
                # Create request body
                data = json.load(StringIO(on_target_uploaded_file.getvalue().decode("utf-8")))
                request_body = parse_obj_as(SitesList, data).dict()
                all_result = load_data(1, request_body, st.session_state.server_url)
                if all_result:
                    process_data(all_result)
            else:
                st.error("File name is not in the correct format. File must be JSON type, "
                         "and contain only letters and numbers")
        elif st.session_state.sequence:
            # input validation
            site_obj = parse_obj_as(List[Site], [{
                "sequence": st.session_state.sequence, "mismatch": st.session_state.mismatch}])
            site_list_obj = SitesList(pam=st.session_state.pam, location=st.session_state.pam_location == "Downstream",
                                      pattern_dna_bulge=st.session_state.dna_bulge, pattern_rna_bulge=st.session_state.rna_bulge,
                                      sites=site_obj, search_tools=st.session_state.tools)

            # Build request body
            request_body = site_list_obj.dict()
            request_body["db_list"] = st.session_state.dbs
            all_result = load_data(1, request_body, st.session_state.server_url)
            if all_result:
                process_data(all_result)
        else:
            pass
