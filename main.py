import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2023 QS World University Rankings", page_icon=":post_office:")
st.title("2023 QS WORLD UNIVERSITY RANKINGS")
data = pd.read_csv("2023 QS World University Rankings.csv")


location = st.selectbox("Pick any country", sorted(tuple(data["location"].unique())))
category = st.selectbox("Pick one of these categories",("Academic Reputation","Employer Reputation",
                                                        "Faculty Student Ratio","Citations per Faculty",
                                                        "International Faculty Ratio","International Students Ratio",
                                                        "International Research Network","Graduate Employability Rankings"))
display = st.button("Show")

def clean(group, loc):
    df = data[data["location"] == loc]
    df = df[["institution", group]].sort_values(by=group, ascending=False).reset_index()
    df.rename(columns = {"index": "overall rank"}, inplace=True)
    return df

def height_graph(df):
    return None if df.shape[0] < 6 else df.shape[0]*35+100

try:
    if display:
        if category != "Overall Rank":
            new_category = ""
            for i in range(category.count(" ") + 1):
                new_category = new_category + category.split()[i][0]
            new_category = new_category.lower() + " score"
        else:
            new_category = category.split()[1]

        df = clean(new_category,location)

        fig_category = px.bar(df, x=new_category, y="institution", orientation="h",template="plotly_white",
                              title=f"<b>Best University\'s {category} Score in {location}</b>",
                              height=height_graph(df))
        fig_category.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)),
                                   yaxis={'categoryorder':'total ascending'})

        left_col, right_col = st.columns(2)
        left_col.table(df)
        right_col.plotly_chart(fig_category, use_container_width=True)
except:
    st.error("An error occured")