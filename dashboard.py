import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("🛒 E-Commerce Fraud Detection Dashboard")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("results/customer_risk.csv")

# ------------------ CREATE RISK CATEGORY ------------------
def risk_category(score):
    if score <= 33:
        return "Low"
    elif score <= 66:
        return "Medium"
    else:
        return "High"

df["risk_category"] = df["risk_score"].apply(risk_category)

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("Filters")

selected_risk = st.sidebar.multiselect(
    "Select Risk Category",
    options=df["risk_category"].unique(),
    default=df["risk_category"].unique()
)

filtered_df = df[df["risk_category"].isin(selected_risk)]

# ------------------ METRICS ------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(filtered_df))
col2.metric("Fraud Customers", len(filtered_df[filtered_df["anomaly"] == -1]))
col3.metric("Normal Customers", len(filtered_df[filtered_df["anomaly"] == 1]))

# Fraud percentage
fraud_percent = (
    len(filtered_df[filtered_df["anomaly"] == -1]) / len(filtered_df) * 100
    if len(filtered_df) > 0 else 0
)

st.metric("Fraud Percentage", f"{fraud_percent:.2f}%")

st.markdown("---")

# ------------------ RISK SEGMENTATION ------------------
st.subheader("Customer Risk Segmentation")

risk_counts = filtered_df["risk_category"].value_counts()

col1, col2, col3 = st.columns(3)

col1.metric("Low Risk Customers", risk_counts.get("Low", 0))
col2.metric("Medium Risk Customers", risk_counts.get("Medium", 0))
col3.metric("High Risk Customers", risk_counts.get("High", 0))

fig2 = px.pie(
    filtered_df,
    names="risk_category",
    title="Risk Category Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ------------------ RISK SCORE DISTRIBUTION ------------------
st.subheader("Risk Score Distribution")

fig = px.histogram(filtered_df, x="risk_score", nbins=50)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ------------------ TOP RISK CUSTOMERS ------------------
st.subheader("Top 10 High Risk Customers")

top_risk = filtered_df.sort_values("risk_score", ascending=False).head(10)
st.dataframe(top_risk)

st.markdown("---")

# ------------------ DOWNLOAD BUTTON ------------------
st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_customer_data.csv",
    mime="text/csv"
)

# ------------------ MODEL INFO ------------------
st.markdown("## 🔍 Model Information")
st.write("""
This fraud detection system uses the Isolation Forest algorithm
to detect anomalous customers based on transaction behavior.

- Anomaly = -1 → Fraud  
- Anomaly = 1 → Normal  
""")

# ------------------ BUSINESS INSIGHTS ------------------
st.markdown("## 📊 Business Insights")

total_customers = len(filtered_df)
fraud_customers = len(filtered_df[filtered_df["anomaly"] == -1])
high_risk = len(filtered_df[filtered_df["risk_category"] == "High"])

st.write(f"""
- Total customers analyzed: **{total_customers}**
- Fraud detected customers: **{fraud_customers}**
- High risk customers: **{high_risk}**
- Fraud rate: **{fraud_percent:.2f}%**

### Recommendations:
- Monitor high-risk customers closely.
- Apply transaction limits to high-risk users.
- Use multi-factor authentication for suspicious behavior.
- Review flagged accounts manually before blocking.
""")
