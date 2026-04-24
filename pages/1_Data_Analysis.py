import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Analysis", layout="wide")

st.title("📊 Detailed Data Analysis")

# Load data
df = pd.read_csv("results/customer_risk.csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

st.subheader("Risk Score Distribution")
fig = px.histogram(df, x="risk_score", nbins=50)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Anomaly Distribution")
fig2 = px.pie(df, names="anomaly", title="Fraud vs Normal Customers")
st.plotly_chart(fig2, use_container_width=True)
