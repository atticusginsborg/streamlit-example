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

event_user.columns = pd.Series(event_user.columns).str.replace(r"\d_", "", regex=True).replace("_", " ", regex=True)

merged_table = pd.merge(event_user, event_attendees, how="inner", left_on="phone number", right_on="phone number")

columns_to_keep = ["name_x", "What is your Cal SID (student ID)?", "identity",]
final_table = merged_table[columns_to_keep]
# updating column names
final_table.columns = ["name_x", "SID", "identity"]
new_file_name = "event_user_with_SID.csv"
download = st.download_button("Download Merged Data", final_table.to_csv(new_file_name))
