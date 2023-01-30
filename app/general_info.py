import logging
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from app.utills import get_off_target, clear_session_information, download_dataframe, get_flashfry_score
from const import HELP_STRING_MAP, FULL_NAME_MAP, COLUMNS_NAME_MAP
from st_aggrid import GridOptionsBuilder, AgGrid, JsCode

log = logging.getLogger("off-risk-ui-log")


def process_data(all_result):
    """
    Process and present all the result in the Web UI
    :param all_result: AllDbResult object
    """
    st.info("Processing results from the server")
    # Create circular graph

    off_target_df = get_off_target()
    flashfry_score_df = get_flashfry_score()
    if len(off_target_df.index) == 0:
        st.error("There is no result from the server - nothing to show")
        return
    # Create flashfry score table
    create_flashfry_score_table(flashfry_score_df)

    # Create off_target table
    create_off_target_table(off_target_df)

    # Plt risk score
    plot_risk_score(off_target_df["risk_score"].value_counts())

    # Present the different DBs information
    st.title("Detailed biological information")
    if all_result:
        hit_id = list()
        for db in all_result:
            db_name = db.replace("_", " ").replace("result list", "").strip()
            db_full_name = FULL_NAME_MAP[db_name]
            help_string = HELP_STRING_MAP[db_name]
            columns_name = COLUMNS_NAME_MAP[db_name]
            st.button("{} database".format(db_full_name),
                      help=help_string)

            if all_result[db]:
                for db_df in all_result[db]:
                    if (db_df["type"] == "DataFrame") and (db_df["description"] == "Complete result"):
                        current_df = pd.DataFrame.from_dict(db_df["data"], orient="columns")
                        log.info("Presenting results for {}".format(db))
                        current_df.sort_values(by=["off_target_id"], inplace=True)
                        # current_df_rename = current_df.rename(columns=str.title, inplace=True)
                        # current_df_rename.columns = current_df_rename.columns.str.replace("_", " ")
                        current_df_rename = current_df.rename(columns=columns_name)
                        gb_current_db = GridOptionsBuilder.from_dataframe(current_df_rename)

                        gb_current_db.configure_pagination()
                        gb_current_db.configure_default_column(groupable=True, filterable=False, sorteable=False,
                                                               editable=True)
                        grid_options_current_db = gb_current_db.build()

                        AgGrid(current_df_rename, gridOptions=grid_options_current_db, enable_enterprise_modules=True)
                        download_dataframe(current_df, db_name)

                        # Additional information
                        if db == "Protein_Atlas_result_list":
                            process_protein_atlas(current_df)

                        elif db == "RBP_result_list":
                            process_rbp(current_df)

                        elif db == "GENCODE_result_list":
                            process_gencode(current_df)

                        st.markdown("---")

                        # Get all present ID
                        current_df_id_list = list(current_df["off_target_id"].unique())
                        hit_id = hit_id + current_df_id_list
            else:
                st.text("There are no Result for this database")
                st.markdown("---")

        # Find missing ID
        off_target_read_only = get_off_target()
        off_target_id_list = off_target_read_only.index
        off_target_id_list = [int(item) for item in off_target_id_list]
        missing_id = list(set(off_target_id_list) - set(hit_id))
        if missing_id:
            st.subheader(f"The following off-target ID did not match in any DB:")
            missing_off_target = off_target_read_only.iloc[missing_id].sort_index()
            AgGrid(missing_off_target[["chromosome", "start", "end", "off_target_id"]])

            download_dataframe(missing_off_target, "Missing_id")
            st.markdown("---")

        log.info("Finish. Deleting the saved response and off-target")
        clear_session_information()

    else:
        st.warning("There is no results to process")


def create_off_target_table(off_target_df):
    st.title("Off-targets Summary")
    columns_name = COLUMNS_NAME_MAP["OFF_TARGET"]
    off_target_df = off_target_df.rename(columns=columns_name)

    gb = GridOptionsBuilder.from_dataframe(off_target_df)
    gb.configure_pagination()
    gb.configure_default_column(filterable=False, sorteable=False, editable=True)

    cell_renderer = JsCode('''
                function(params) {
                    let myArray = params.value.split(',');
                    let response = '';
                    for (let i = 0; i < myArray.length; i++) {
 
                        let tmp = '<a href="https:\/\/www.ensembl.org\/Homo_sapiens\/Gene\/Summary?g=' + myArray[i] + '" target="_blank">'+ myArray[i] + '</a>,';
                        response +=  tmp;
  
                    }
                    return response.replace(/,$/, '');
                }
                ''')

    gb.configure_columns(["Gene Ensembl Id", "Remap Epd Gene Ensembl Id", "Enhancer Atlas Gene Ensembl Id"],
                         cellRenderer=cell_renderer)

    cellstyle_jscode = JsCode("""
        function(params){
            if (params.data.Risk_Score == 'High_coding') {
                return {
                    'backgroundColor': 'firebrick',
                }
            }
            if (params.data.Risk_Score == 'Medium_coding') {
                return{
                    'backgroundColor': 'red',
                }
            }
            if (params.data.Risk_Score == 'Low_coding') {
                return{
                    'backgroundColor': 'lightsalmon',
                }
            }
            if (params.data.Risk_Score == 'Medium_regulatory') {
                return{
                    'backgroundColor': 'orange',
                }
            }
            if (params.data.Risk_Score == 'Low_regulatory') {
                return{
                    'backgroundColor': 'bisque',
                }
            }
        }
        """)
    gb.configure_columns(off_target_df, cellStyle=cellstyle_jscode)
    grid_options = gb.build()
    AgGrid(
        off_target_df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True
    )
    download_dataframe(off_target_df, "Off target result")


def plot_risk_score(off_target_score_count):
    """
    Create pie chart for the Risk Score information
    :param off_target_score_count: pandas Sireis count of the
    """
    col = st.columns(3)
    color_map = {"High_coding": "firebrick", 'Medium_coding': "red", 'Low_coding': "lightsalmon",
                 'Medium_regulatory': "orange", "Low_regulatory": 'bisque', "": "white"}
    colors = [color_map[x] for x in off_target_score_count.index]
    fig, ax = plt.subplots()
    total = sum(off_target_score_count)
    ax.pie(off_target_score_count, labels=off_target_score_count.index,
           autopct=lambda p: '{:.0f}'.format(p * total / 100),
           colors=colors, textprops={'fontsize': 8},
           wedgeprops={"edgecolor": "black", 'linewidth': 0.5})
    ax.set_title("Score sum", fontsize=14)
    plt.tight_layout()
    col[1].pyplot(fig)


def create_flashfry_score_table(flashfry_score_df):
    """
    Present in AgGrid table FlashFry information.
    :param flashfry_score_df: FlashFry dataframe information.
    """
    if flashfry_score_df is not None and len(flashfry_score_df.index) != 0:
        st.title("FlashFry Score Summary")
        flashfry_score_df.rename(columns=str.title, inplace=True)
        gb_flashfry_score = GridOptionsBuilder.from_dataframe(flashfry_score_df)
        gb_flashfry_score.configure_pagination()
        gb_flashfry_score.configure_default_column(groupable=True, filterable=False, sorteable=False,
                                                   editable=True)
        grid_options_flashfry_score = gb_flashfry_score.build()

        AgGrid(flashfry_score_df, gridOptions=grid_options_flashfry_score, enable_enterprise_modules=True)
        download_dataframe(flashfry_score_df, "FlashFry_score")


def process_gencode(current_df):
    """
    Present gencode statistic in pie chart
    :param current_df: GENCODE dataframe
    """
    coding = ("protein_coding", "IG_V_gene", "IG_C_gene", "IG_J_gene", "TR_C_gene",
              "TR_J_gene", "TR_V_gene", "TR_D_gene", "IG_D_gene")
    non_coding = ("miRNA", "lncRNA", "snRNA", "misc_RNA", "snoRNA", "scaRNA", "sRNA",
                  "ribozyme", "vault_RNA", "Mt_tRNA", "Mt_rRNA")

    gencode_gene_type_count = current_df["gene_type"].value_counts()

    # todo: we need to make it more efficient
    gencode_stat_df_list = dict()
    gencode_stat_df_list.update({"Gene Type distribution": gencode_gene_type_count})
    gencode_stat_df_list.update({
        "Segment distribution for coding": current_df[current_df.gene_type.isin(coding)]["segment"].value_counts()})
    gencode_stat_df_list.update(
        {"Segment distribution for non coding": current_df[current_df.gene_type.isin(non_coding)]["segment"].
            value_counts()})
    col = st.columns(3)
    i = 0
    for stat in gencode_stat_df_list:
        if not gencode_stat_df_list[stat].empty:
            fig, ax = plt.subplots()
            total = sum(gencode_stat_df_list[stat])
            ax.pie(gencode_stat_df_list[stat], labels=gencode_stat_df_list[stat].index,
                   autopct=lambda p: '{:.0f}'.format(p * total / 100),
                   colors=plt.get_cmap("Accent").colors, textprops={'fontsize': 8})
            ax.set_title(stat, fontsize=14)
            plt.tight_layout()
            col[i].pyplot(fig)
            i += 1


def process_protein_atlas(current_df):
    """
    Process Protein Atlas result as heatmap
    :param current_df: Protein Atals dataframe
    """
    tmp_current_df = current_df.drop(columns=["gene_ensembl_id"], axis=1)
    tmp_current_df = tmp_current_df.fillna("None").set_index("gene_symbol", append=False)
    # create dictionary with value to integer mappings
    value_to_int = {value: i for i, value in
                    enumerate(["Not representative", "None", "Not detected", "Low", "Medium", "High"])}

    current_df_new = tmp_current_df.replace(value_to_int).drop(["off_target_id"], axis=1).T
    f, ax = plt.subplots(figsize=(10, 30))
    cbar_kws = {"orientation": "horizontal", "pad": 0.05, "aspect": 30}
    sns.set(font_scale=0.6)
    sns.heatmap(data=current_df_new, ax=ax, linewidths=2, cmap="RdPu", cbar_kws=cbar_kws, xticklabels=1, yticklabels=1)

    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks([0, 1, 2, 3, 4, 5])
    colorbar.set_ticklabels(["Not representative", "None", "Not detected", "Low", "Medium", "High"])
    plt.tight_layout()
    st.pyplot(f)


def process_rbp(current_df):
    """
    Process RBP result as heatmap
    :param current_df: RBP dataframe returned from offRisk server
    """
    current_df = current_df.drop(["off_target_id", "gene_ensembl_id"], axis=1)
    current_df.rename(columns={"gene_symbol": "Gene Symbol"}, inplace=True)
    current_df = current_df.set_index("Gene Symbol")

    f, ax = plt.subplots()
    colors = ["white", "black"]
    cmap = LinearSegmentedColormap.from_list("", colors, 2)
    sns.set(font_scale=0.5)
    sns.heatmap(data=current_df, ax=ax, linewidths=1, cmap=cmap, xticklabels=1, yticklabels=1, cbar=False, square=True)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    st.write(f)
