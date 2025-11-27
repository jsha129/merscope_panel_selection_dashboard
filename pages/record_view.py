# ---- File: pages/record_view.py ----
import streamlit as st
import pandas as pd
from io import BytesIO
import re
import matplotlib.pyplot as plt

st.set_page_config(page_title="Record View", layout='wide')

if "df" not in st.session_state:
    st.error("Please go back and upload a file.")
    st.stop()



df = st.session_state.df
idx = st.session_state.get("idx", 0)
record = df.iloc[idx]

with st.sidebar:
    gene_nav_selection = st.selectbox('Jump to Gene: ', df['gene'])
    if st.button("Go"):
        # st.session_state.idx = 
        idx2 = list(df[ df['gene'] == gene_nav_selection ].index)[0]
        st.session_state.idx =  idx2
        st.rerun()
    st.html('<b> {}  Genes selected: </b>'.format(str( df[df['isFinalInclude'] ].shape[0] ) ) )
    st.dataframe(df[ df['isFinalInclude']].reset_index()['gene'])


df_bargraph = df[ [c for c in df.columns if re.search("^g\d+.*", c) ] ]
st.title(f"Record {idx + 1} / {len(df)}")

# st.html(df.columns)

st.html('<hr />')
col1, col2, col3, col4 = st.columns(4)
col1_fields  = ["gene", 'is_member_of_Maria_genelist', 'gene_marker_of_cells', 'description', 'gene_summary'] # immutable
col2_fields = []
inactive_chkbox_fields = [c for c in df.columns if re.search("DE", c) and c != 'DE_in_some_cells' ]
# ['is_DE_BS_EC'] # inactive checkbox
col2_fields.extend(inactive_chkbox_fields)
col2_fields.sort()
col3_fields = [c for c in df.columns if re.search("PATHWAY", c) ]



updated_values = {}

with col1:
    st.html("<h3 style='color: MediumBlue'> Gene Info </h3>") # immutable fields
    st.html(col1_fields)
    for col in col1_fields:
        st.html("<b>{}: </b> {}".format(col, str(record[col]) )) 
        
    st.html("<hr /><h3 style='color: MediumBlue'> Normalised Expression in clusters / cell types</h3>")
    st.bar_chart(df_bargraph.iloc[idx], x_label="Normalised Exp", horizontal = True)
    
with col2:
    st.html("<h3 style='color: MediumBlue'>Selection Criteria</h3>")
    st.html('DIPG vs Control in Bstem. "c1" means cluster 1 of unfiltered scRNA data')
    for col in col2_fields:
        if col == 'isFinalInclude':
            updated_values[col] = st.checkbox('Add to Panel Design', record[col], key = f"{col}_{idx}") 
        elif col in inactive_chkbox_fields:
            st.checkbox(col, record[col], disabled= True)
        else:
            st.html("<b>{}: </b> {}".format(col, str(record[col]) ))
    updated_values['Notes'] = st.text_area('Notes', record['Notes'], height = "stretch", key = f"Notes_{idx}")
    updated_values['isFinalInclude'] = st.checkbox('Add to Panel Design', record['isFinalInclude'], key = f"isFinalInclude_{idx}") 


with col3:
    st.html("<h3 style='color: MediumBlue'>Involvement in Pathways </h3>")
    for col in col3_fields[:12]:
        st.checkbox(re.sub('PATHWAY_', '', col), record[col], disabled= True)

with col4:
    for col in col3_fields[12::]:
        st.checkbox(re.sub('PATHWAY_', '', col), record[col], disabled= True)
       
    

## -- navigations
#! reconrds are autosaved
col_prev, col_next, col_download = st.columns(3 )

with col_prev:
    if st.button("Previous"):
        for key,item in updated_values.items():
             df.at[st.session_state.idx, key] = item
        st.session_state.idx = max(0, idx - 1)
        st.rerun()

# with col_save:
#     if st.button("Save"):
#         for key,item in updated_values.items():
#              df.at[st.session_state.idx, key] = item
#         st.session_state.df = df
#         st.success("Record updated!")

with col_download: 
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()
    
    st.download_button(
        label="⬇️ Download Updated Excel",
        data= to_excel(df),
        file_name="updated_data.xlsx",
        type="primary",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


with col_next:
    if st.button("Next"):
        for key,item in updated_values.items():
             df.at[st.session_state.idx, key] = item
        st.session_state.idx = min(len(df) - 1, idx + 1)
        st.rerun()
