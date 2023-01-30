import json
import logging
import os
import re
import sys
from io import StringIO
from typing import List
import streamlit as st
from pydantic.tools import parse_obj_as

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(CURRENT_DIR))

from app.const import ON_TARGET_UPLOAD_HELP
from app.general_info import process_data
from app.object_def import Site, SitesList
from app.utills import load_data, get_server_db_info

log = logging.getLogger("off-risk-ui-log")


hide_streamlit_style = """
    <style>
    footer {visibility: hidden; padding:0}
"""

# Hide streamlit style (footer)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title('On target page')
st.header('Please choose server and databases for on-target analysis')
server_name_url, selected_options = get_server_db_info()
st.markdown("---")

st.header('off-target search tool')
tools_selection = st.multiselect("Please select off-target search tool", ["flashfry", "cas_offinder"], ["flashfry"])
st.markdown("---")

st.header('Fill the following for on target analysis. Sequence is a mandatory field')
col1, col2, col3 = st.columns((3, 1, 1))
pattern = col1.text_input("Pattern", "NNNNNNNNNNNNNNNNNNNNNGG", max_chars=50)
dna_bulge = col2.text_input("DNA bulge", 0, max_chars=2)
rna_bulge = col3.text_input("RNA bulge", 0, max_chars=2)
col1, col2 = st.columns((3, 1))
sequence = col1.text_input("Sequence", "", max_chars=50)
mismatch = col2.number_input("Mismatch", value=4, min_value=0, max_value=15)
st.markdown("---")

st.header('Upload json file for on-target analysis')
on_target_uploaded_file = st.file_uploader("On-Target file upload", type=[".json"], help=ON_TARGET_UPLOAD_HELP)
st.markdown("---")

if st.button("Run"):
    if not on_target_uploaded_file and not sequence:
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
                all_result = load_data(1, request_body, server_name_url)
                process_data(all_result)
            else:
                st.error("File name is not in the correct format. File must be JSON type, "
                         "and contain only letters and numbers")
        elif sequence:
            # input validation
            site_obj = parse_obj_as(List[Site], [{
                "sequence": sequence, "mismatch": mismatch}])
            site_list_obj = SitesList(pattern=pattern, pattern_dna_bulge=dna_bulge, pattern_rna_bulge=rna_bulge,
                                      sites=site_obj, search_tools=tools_selection)

            # Build request body
            request_body = site_list_obj.dict()
            request_body["db_list"] = selected_options
            all_result = load_data(1, request_body, server_name_url)
            process_data(all_result)
        else:
            pass
