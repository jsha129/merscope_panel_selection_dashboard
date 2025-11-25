import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

temp_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = [ temp_letters[i] for i in range(25) ]

## --
df_bargraph = pd.DataFrame( {"Category": ["A", "B", "C", "D"], "Value": [10, 23, 7, 15]} )

## -- main app
st.set_page_config(page_title="Gene Selection Page for Merscope Panel", layout="wide")

# ------------------------------------------
# USER CONFIG: Choose which columns appear in column 1
# ------------------------------------------
col1_fields  = ["Gene", "Official_Symbol", "Commonality", "Target Cell type", "g0.Endothelial.Mouse_scRNA"]
immutable_fields = ['Gene']

# ------------------------------------------
# Checkboxes will be detected if column dtype is bool OR if name contains these keywords
# ------------------------------------------
checkbox_keywords = ['isFinalInclude', 'isDE','isCellMarker']
checkbox_keywords = [ c.lower() for c in checkbox_keywords ]

# ------------------------------------------
# App starts here
# ------------------------------------------
st.title("Gene Selection Page for Merscope Panel") 

# uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if "df" not in st.session_state:
    st.session_state.df = None

if "row" not in st.session_state:
    st.session_state.row = 0

# if uploaded_file:
#     df = pd.read_excel(uploaded_file, sheet_name = "Sheet1")
#     st.session_state.df = df

if st.session_state.df is not None:
    df = st.session_state.df
    num_rows = len(df)

    st.write(f"**Total records:** {num_rows}")
    st.html('<b>Gene starts with: </b>' + '  '.join(letters))

    # --- Navigation buttons ---
    colA, colB, colC = st.columns([1,1,1])

    with colA:
        if st.button("⬅️ Previous") and st.session_state.row > 0:
            st.session_state.row -= 1

    with colB:
        st.write(f"**Record {st.session_state.row + 1} of {num_rows}**")

    with colC:
        if st.button("Next ➡️") and st.session_state.row < num_rows - 1:
            st.session_state.row += 1

    current_row_data = df.iloc[st.session_state.row]

    st.subheader("Record Details")

    # --- Two column form layout ---
    left_col, middle_col, right_col = st.columns(3)

    # Split fields into two groups
    col1_fields = [c for c in df.columns if c in col1_fields ]
    col2_fields = [c for c in df.columns if c not in col1_fields ]

    updated_values = {}

    # -----------------------------
    # Column 1 fields
    # -----------------------------
    with left_col:
        st.markdown("### Column 1 Fields")
        for col in col1_fields:
            val = current_row_data[col]

            # Checkbox rules
            is_checkbox = ( isinstance(val, bool) or any(k in col.lower() for k in checkbox_keywords) )

            if is_checkbox:
                updated_values[col] = st.checkbox(col, value=bool(val))
            else:
                # updated_values[col] = st.text_input(col, value=str(val))
                updated_values[col] = st.html("<b>{}: </b> {}".format(col,str(val)))

    # -----------------------------
    # Column 2 fields
    # -----------------------------
    with middle_col:
        st.markdown("### Column 2 Fields")
        for col in col2_fields:
            val = current_row_data[col]
            # Checkbox rules
            is_checkbox = ( isinstance(val, bool) or any(k in col.lower() for k in checkbox_keywords) )

            if is_checkbox:
                updated_values[col] = st.checkbox(col, value=bool(val))
            else:
                updated_values[col] = st.text_input(col, value=str(val))
    
    with right_col:
        # -- this is bar graph
        plt.rcParams['font.size'] = 8 # Default font size for general text
        plt.rcParams['axes.labelsize'] = 10  # Font size for x and y axis labels
        plt.rcParams['xtick.labelsize'] = 6  # Font size for x-axis tick labels
        plt.rcParams['ytick.labelsize'] = 6  # Font size for y-axis tick labels
        plt.rcParams['legend.fontsize'] = 8  # Font size for legend text
        plt.rcParams['figure.titlesize'] = 8  # Font size for figure titles
        plt.rcParams['axes.titlesize'] = 6  # Font size for subplot titles

        fig, ax = plt.subplots(figsize = (4,6))
        ax.bar(df_bargraph["Category"], df_bargraph["Value"])
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")
        ax.set_title("Gene Expression")
        # st.subheader("Bar Chart")
        st.pyplot(fig)

    # --- Save button ---
    if st.button("💾 Save Changes"):
        for col, new_value in updated_values.items():

            # Convert checkbox text to boolean if necessary
            if df[col].dtype == bool:
                new_value = bool(new_value)

            df.at[st.session_state.row, col] = new_value

        st.session_state.df = df
        st.success("Record updated!")

    # --- Download updated Excel ---
    # output = df.to_excel(index=False)
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()
    
    st.download_button(
        label="⬇️ Download Updated Excel",
        data= to_excel(df),
        file_name="updated_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    options = df['Gene']
    selected_gene = st.sidebar.selectbox(
        "Jump to a gene:",
        options
    )

