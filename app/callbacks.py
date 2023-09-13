import streamlit as st
from const import DB_NAME_LIST

def on_change_server():
        st.session_state.server_url = "{}:{}".format(st.session_state.server_address, st.session_state.server_port)

def on_select_all():
    if st.session_state.is_select_all:
        st.session_state.dbs = DB_NAME_LIST

def on_change_dbs_selection():

    if len(st.session_state.dbs) == len(DB_NAME_LIST) and not st.session_state.is_select_all:
        st.session_state.is_select_all = True
    elif len(st.session_state.dbs) != len(DB_NAME_LIST) and st.session_state.is_select_all:
        st.session_state.is_select_all = False

