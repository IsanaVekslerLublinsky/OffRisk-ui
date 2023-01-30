import base64
import io
import subprocess
import logging
import httpx
import os
import sys
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from const import LOG_PATH, SERVER_MAP, DB_NAME_LIST

log = logging.getLogger("off-risk-ui-log")


def get_server_db_info():
    col1, col2 = st.columns(2)

    server_name = col1.selectbox("Select server", ("CRISPR-il", "Local", "Custom"))
    if server_name == "Custom":
        server_address = col1.text_input("Server-name", "localhost", max_chars=50)
        server_port = col1.text_input("Port", "8123", max_chars=4)
        server_name_url = SERVER_MAP[server_name].format(server_address, server_port)
    else:
        server_name_url = SERVER_MAP[server_name]

    container = col2.container()
    select_all = col2.checkbox("Select all")
    if select_all:
        selected_options = container.multiselect("Select databases:", DB_NAME_LIST, DB_NAME_LIST)
    else:
        selected_options = container.multiselect("Select databases:", DB_NAME_LIST, ["gencode"])

    return server_name_url, selected_options


def load_data(case, request_body, chosen_server_name):
    """
    Load the user input and get the off-target result for offRisk server
    :param case: which use case to run
    :param request_body: the request body to send
    :param chosen_server_name: The server DNS or IP name to send the request to
    :return: the all_result response from the offRisk server
    """
    st.info("Sending request")
    all_result_dict = None
    try:
        # on target
        response_body, r_status = None, None
        request_body["request_id"] = get_current_request_id()

        if case == 1:
            log.info("Sending request for on-target")
            # Create request body
            r_status, response_body = handle_post_request(request_body, "on-target",
                                                          chosen_server_name)

        # off target
        if case == 2:
            log.info("Sending request for off-target")

            # send request
            r_status, response_body = handle_post_request(request_body, "off-target",
                                                          chosen_server_name)
        if r_status:
            st.error(f"Error while getting the Response: {response_body}")
        else:
            all_result_dict = build_all_result(response_body)

    except UnicodeDecodeError as e:
        log.error("error in load_data {}".format(e))
        st.error("error loading: {}".format(e))
    return all_result_dict


def handle_post_request(json_as_dictionary, str_of_target, server=SERVER_MAP["Local"]):
    """
    :param server: the server name or IP to send the request to
    :param json_as_dictionary: the user input in json format
    :param str_of_target: off-target / on-target
    :return: response from the server
    """
    log.info("Sending request {} with body {}".format(
        "{}/v1/{}-analyze/".format(server, str_of_target), json_as_dictionary))
    try:
        r = httpx.post("{}/v1/{}-analyze/".format(server, str_of_target), timeout=10000,
                       json=json_as_dictionary)

        if r.status_code == 200:
            log.info("Server returned code: {}".format(r.status_code))
            respond = r.json()
            return 0, respond
        else:
            error_message = BeautifulSoup(r.text).getText()
            log.error("Server returned error code: {}: {}".format(r.status_code, error_message))
            return 1, error_message
    except Exception as e:
        log.error("Error in handle_post_request: {}".format(e))
        return 1, e


def preprocess_omim(genemap2_file_path, mim2gene_file_path):
    """
    Load genemap2.txt and mim2gene.txt. Downloaded on 24/12/2020
    Returns:

    """
    log.info("Preprocessing OMIM data")
    genemap2_df = pd.read_csv(genemap2_file_path, sep="\t", skiprows=3,
                              usecols=(
                                  "# Chromosome", "Genomic Position Start", "Genomic Position End", "MIM Number",
                                  "Phenotypes"))
    # Remove all rows that do not contains any data
    genemap2_df = genemap2_df[~genemap2_df["# Chromosome"].astype(str).str.startswith("#")]

    genemap2_df_bed = genemap2_df.astype(
        {"Genomic Position Start": int, "Genomic Position End": int, "Phenotypes": "string", "MIM Number": int})

    genemap2_df_bed.rename(columns={"# Chromosome": "chromosome", "Genomic Position Start": "start",
                                    "Genomic Position End": "end", "MIM Number": "omim_id",
                                    "Phenotypes": "disease_related"}, inplace=True)
    genemap2_df_bed.dropna(subset=["disease_related"], inplace=True)
    # Merger the Ensembl ID and add it to attributes as the same format in gff
    mim2gene_pd = pd.read_csv(mim2gene_file_path, sep="\t", skiprows=4)
    mim2gene_pd.rename(columns={"# MIM Number": "omim_id",
                                "Ensembl Gene ID (Ensembl)": "gene_ensembl_id"}, inplace=True)

    genemap2_df_bed = genemap2_df_bed.merge(mim2gene_pd, on="omim_id")
    genemap2_df_bed.rename(columns={"Approved Gene Symbol (HGNC)": "gene_symbol"}, inplace=True)

    genemap2_df_bed["inheritance_model"] = ""
    for row in genemap2_df_bed.itertuples():
        current_phenotypes = row.disease_related
        current_inheritance_model = ""
        if current_phenotypes:
            if ("X-linked dominant" in current_phenotypes) | ("X-linked recessive" in current_phenotypes):
                if "X-linked dominant" in current_phenotypes:
                    current_inheritance_model = current_inheritance_model + "X-linked dominant "
                    current_phenotypes = current_phenotypes.replace("X-linked dominant", "")
                if "X-linked recessive" in current_phenotypes:
                    current_inheritance_model = current_inheritance_model + "X-linked recessive "
                    current_phenotypes = current_phenotypes.replace("X-linked recessive", "")
            elif "X-linked" in current_phenotypes:
                current_inheritance_model = current_inheritance_model + "X-linked "
                current_phenotypes = current_phenotypes.replace("X-linked", "")
            if "Autosomal dominant" in current_phenotypes:
                current_inheritance_model = current_inheritance_model + "Autosomal dominant "
                current_phenotypes = current_phenotypes.replace("Autosomal dominant", "")
            if "Autosomal recessive" in current_phenotypes:
                current_inheritance_model = current_inheritance_model + "Autosomal recessive"
                current_phenotypes = current_phenotypes.replace("Autosomal recessive", "")
            genemap2_df_bed.loc[row.Index, "inheritance_model"] = current_inheritance_model.strip()
            genemap2_df_bed.loc[row.Index, "disease_related"] = current_phenotypes.rstrip(" ,{}")
    return genemap2_df_bed.to_csv(sep="\t", index=False,
                                  columns=["gene_ensembl_id", "gene_symbol", "omim_id", "disease_related",
                                           "inheritance_model"]).encode('utf-8')


def separate_id(line):
    if line:
        id_list = line.split(",")
        ensembl_id = [item for item in id_list if "ENSG" in item]
        if len(ensembl_id) > 0:
            if len(ensembl_id) > 1:
                print(
                    "Size of the ensembl ID list is {} when it should be 1. returning only the first one".format(
                        len(ensembl_id)))
            return ensembl_id[0].split(".")[0]


def preprocess_cosmic(cosmic_input_file_path):
    """
    Downloaded on 7/11/2022
    """
    log.info("Preprocessing COSMIC data")
    db_df = pd.read_csv(cosmic_input_file_path)
    db_df.drop(["Entrez GeneId", "Genome Location", "Tier", "Hallmark", "Chr Band", "Cancer Syndrome", "Tissue Type",
                "Mutation Types", "Translocation Partner", "Other Germline Mut", "Other Syndrome"],
               axis=1, inplace=True)
    db_df.rename(columns={"Gene Symbol": "gene_symbol"}, inplace=True)
    db_df["gene_ensembl_id"] = db_df["Synonyms"].apply(lambda s: separate_id(str(s)))
    db_df.drop(["Synonyms"], axis=1, inplace=True)
    db_df.dropna(subset=["Role in Cancer"], inplace=True)
    return db_df.to_csv(sep="\t", index=False).encode('utf-8')


# Global function
def set_off_target_dict(new_off_target_dict):
    """
    Set the off-target result in a global variable
    :param new_off_target_dict: the result off-target from the offRisk server
    """
    log.debug("Setting a new off-targets")

    # Initialization
    off_target = pd.DataFrame.from_dict(new_off_target_dict)
    columns_name = off_target.columns

    if "gene_ensembl_id" in columns_name:
        off_target['gene_ensembl_id'] = [','.join(map(str, item)) for item in
                                         off_target['gene_ensembl_id']]
    if "remap_epd_gene_ensembl_id" in columns_name:
        off_target['remap_epd_gene_ensembl_id'] = [','.join(map(str, item)) for item in
                                                   off_target['remap_epd_gene_ensembl_id']]
    if "enhancer_atlas_gene_ensembl_id" in columns_name:
        off_target['enhancer_atlas_gene_ensembl_id'] = [','.join(map(str, item)) for item in
                                                        off_target['enhancer_atlas_gene_ensembl_id']]

    if "gene_symbol" in columns_name:
        off_target['gene_symbol'] = [','.join(map(str, item)) for item in
                                     off_target['gene_symbol']]
    if "segment" in columns_name:
        off_target['segment'] = [','.join(map(str, item)) for item in
                                 off_target['segment']]
    if "disease_related" in columns_name:
        off_target['disease_related'] = [','.join(map(str, item)) for item in
                                         off_target['disease_related']]
    if "inheritance_model" in columns_name:
        off_target['inheritance_model'] = [','.join(map(str, item)) for item in
                                           off_target['inheritance_model']]

    if "expression_information" in columns_name:
        off_target['expression_information'] = [','.join(map(str, item)) for item in
                                                off_target['expression_information']]
    if "ReMap_EPD" in columns_name:
        off_target['ReMap_EPD'] = [','.join(map(str, item)) for item in off_target['ReMap_EPD']]
    if "cancer_related" in columns_name:
        off_target['cancer_related'] = [','.join(map(str, item)) for item in off_target['cancer_related']]
    if "mir_gene" in columns_name:
        off_target['mir_gene'] = [','.join(map(str, item)) for item in off_target['mir_gene']]
    off_target.drop(columns=["id", "sequence"], inplace=True)
    st.session_state['off_target'] = off_target


def get_off_target():
    """
    :return: get the global off-target result from the offRisk server
    """
    log.debug("Returning off-target")
    if "off_target" in st.session_state:
        return st.session_state['off_target']


def get_flashfry_score():
    """
        :return: get the flashfry scofre result from the offRisk server
        """
    log.debug("Returning FlashFry score")
    if "flashfry_score" in st.session_state:
        return st.session_state['flashfry_score']


def clear_session_information():
    """
    reset the dataframe to be empty
    """
    log.debug("Clearing the current response")
    if "off_target" in st.session_state:
        st.session_state.off_target.drop(st.session_state.off_target.index, inplace=True)
    if "flashfry_score" in st.session_state:
        st.session_state.flashfry_score.drop(st.session_state.flashfry_score.index, inplace=True)


# Global request number
request_id = 1


def get_current_request_id():
    """
    :return: current request_id
    """
    global request_id
    current_id = request_id
    request_id += 1
    return current_id


def build_all_result(response):
    """
    :param response: dictionary represent a json format received from the server
    :return: list of dataframes, each dataframe represent different database, can be change in th future !!!
    """

    try:
        all_result = response["all_result"]
        set_off_target_dict(response["off_targets"])
        if response["flashfry_score"]:
            test = pd.DataFrame.from_dict(response["flashfry_score"])
            st.session_state["flashfry_score"] = test
        return all_result
    except Exception as e:
        log.error("Issue in build_dataframe: {}".format(e))


def run_external_proc(args):
    """
    Run an external program with Popen.
    Args:
        args: The argument to run, a list of string
    """

    function_name = "run_external_proc"
    log.debug("Entering {}".format(function_name))

    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        log.debug("{}: The following command will be run: {}".format(function_name, args))

        while True:
            next_line = proc.stdout.readline().decode("utf-8").strip()
            if next_line == "" and proc.poll() is not None:
                break
            if next_line != "":
                log.info(next_line)

        err, output = proc.communicate()
        exit_code = proc.returncode

        if exit_code == 0:
            log.info(output.decode())
        else:
            log.error("Error in {}.\nCommand is : {}\nError is: {} {}".format(
                function_name, args, output.decode(), err.decode()))
        return exit_code


@st.cache
def init_logger(log_file=LOG_PATH, debug_level=logging.INFO, logger_name=None):
    """
    Init the logger for the program
    :param log_file: the location of the log file
    :param debug_level: the minimum log level
    :param logger_name: the name of the logger in the module
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(debug_level)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(debug_level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(fh)


def download_dataframe(df, df_name):
    """
    Present link for download dataframe as csv file or xslx
    :param df: Dataframe to download
    :param df_name: The name of the database
    """
    col1, col2 = st.columns((1, 1))
    with col1:
        st.markdown(download(df=df, file_type='csv', file_name=df_name), unsafe_allow_html=True)
    with col2:
        st.markdown(download(df=df, file_type='xslx', file_name=df_name), unsafe_allow_html=True)


def download(df, file_type, file_name="data"):
    """

    :param df: Dataframe to download
    :param file_type: Type to download - csv or xslx
    :param file_name: The name for the file downloaded
    :return:
    """
    if file_type == 'csv':
        csv_to_download = df.to_csv(index=False)
        b64 = base64.b64encode(csv_to_download.encode()).decode()
        link_str = \
            f'<a href="data:file/csv;base64,{b64}" download="{file_name}.csv">download your results as csv file</a>'
        return link_str
    else:
        # case for xslx file
        towrite = io.BytesIO()
        df.to_excel(towrite, encoding='utf-8', index=False, header=True)
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()
        link_str = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' \
                   f'{b64}" download="{file_name}.xlsx">Download excel file</a>'
        return link_str
