import logging
import os
import re
import sys
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(CURRENT_DIR))

from app.utills import preprocess_omim, preprocess_cosmic


log = logging.getLogger("off-risk-ui-log")

hide_streamlit_style = """
    <style>
    footer {visibility: hidden; padding:0}
"""

st.write('If you wish to use COSMIC and OMIM database, please download the files, and only on the first use run '
         'preprocessing for them here:\n'
         'Please enter the full name of the file and place it in the relevant folder - '
         'OMIM files in OMIM folder, and COSMIC file in COSMIC folder')
val_genemap2, val_mim2gene, val_cosmic, omim_output_path, cosmic_output_path = None, None, None, None, None
col1, col2 = st.columns(2)

genemap2_uploaded_file = col1.file_uploader("OMIM genemap2 file upload", type=[".txt"])
mim2gene_uploaded_file = col1.file_uploader("OMIM mim2gene file upload", type=[".txt"])
cosmic_uploaded_file = col2.file_uploader("COSMIC file upload", type=[".csv"])

if col1.button("Preprocess OMIM"):
    if genemap2_uploaded_file:
        val_genemap2_uploaded_file = re.match(r"[A-Za-z0-9_\-\\]+\.txt", genemap2_uploaded_file.name)
        val_genemap2 = val_genemap2_uploaded_file and val_genemap2_uploaded_file.group() == genemap2_uploaded_file.name
        if not val_genemap2:
            st.error("File name is not in the correct format. File must be txt type, "
                     "and contain only letters and numbers")
    if mim2gene_uploaded_file:
        val_mim2gene_uploaded_file = re.match(r"[A-Za-z0-9_\-\\]+\.txt", mim2gene_uploaded_file.name)
        val_mim2gene = val_mim2gene_uploaded_file and val_mim2gene_uploaded_file.group() == mim2gene_uploaded_file.name
        if not val_mim2gene:
            st.error("File name is not in the correct format. File must be txt type, "
                     "and contain only letters and numbers")

    if val_genemap2 and val_mim2gene:
        omim_output_path = preprocess_omim(genemap2_uploaded_file, mim2gene_uploaded_file)

    col1.download_button(
        label="Download OMIM file",
        data=omim_output_path,
        file_name='omim.csv',
        mime='text/csv',
    )

if col2.button("Preprocess COSMIC"):
    if cosmic_uploaded_file:
        val_cosmic_uploaded_file = re.match(r"[A-Za-z0-9_\-\\]+\.csv", cosmic_uploaded_file.name)
        val_cosmic = val_cosmic_uploaded_file and val_cosmic_uploaded_file.group() == cosmic_uploaded_file.name
        if not val_cosmic:
            st.error("File name is not in the correct format. File must be csv type, "
                     "and contain only letters and numbers")

    if val_cosmic:
        cosmic_output_path = preprocess_cosmic(cosmic_uploaded_file)

    col2.download_button(
        label="Download COSMIC file",
        data=cosmic_output_path,
        file_name='cosmic.csv',
        mime='text/csv',
    )

