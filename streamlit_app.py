import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))


event_attendees = st.file_uploader("Upload Attendance Data", type="csv")
event_user = st.file_uploader("Upload Evant Data", type="csv")

if (event_attendees is not None) and (event_user is not None):
    event_attendees = pd.read_csv(event_attendees)
    event_user = pd.read_csv(event_user)
    event_user.columns = pd.Series(event_user.columns).str.replace(r"\d_", "", regex=True).replace("_", " ", regex=True)

    #creating identity column
    event_user["identity"] = event_user.fillna("").iloc[:, 10] + event_user.fillna("").iloc[:, 11]
    
    col1 = st.multiselect("Columns in attendance Data", event_attendees.columns)
    col2 = st.multiselect("Columns in Evant Data", event_user.columns)
    condition_to_continue = ((len(col1) > 1) and ("What is your SID (student ID)?" in col2) and ("phone number" in col1) and ("phone number" in col2) and ("identity" in col2))
    if "phone number" not in col1:
        st.warning("Make sure to include the phone number in first table so data can be merged")
    elif "phone number" not in col2:
        st.warning("Make sure to include the phone number in second table so data can be merged")
    elif "What is your SID (student ID)?" not in col2:
        st.warning("Make sure to include the student ID info")
    elif if sum(pd.Series(col2).str.contains("identity")) == 0:
        st.warning("Make sure to include the Jewish identity info")
    else:
        merged_table = pd.merge(event_user[col2], event_attendees[col1], how="inner", left_on="phone number", right_on="phone number")
        
        columns_to_keep = st.multiselect("Columns in Merged Data", merged_table.columns)
        if len(columns_to_keep) < 3:
            st.warning("You have not selected enough columns")
        elif "What is your SID (student ID)?" not in columns_to_keep:
            st.warning("You forgot to include the SID column")
        final_table = merged_table[columns_to_keep]
        # updating column names
        # final_table.columns = ["name", "SID", "Jewish identity"]
        new_file_name = "event_user_with_SID.csv"
        data_as_csv= final_table.to_csv(index=False).encode("utf-8")
        download = st.download_button(
            "Download Merged Data as CSV", 
            data_as_csv, 
            new_file_name,
            "text/csv",
            key=new_file_name,
        )    
else:
    st.warning('Please upload a CSV file to continue.')
