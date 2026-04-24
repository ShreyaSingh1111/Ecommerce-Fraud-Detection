import streamlit as st

st.set_page_config(page_title="Model Info", layout="wide")

st.title("🔍 Model Information")

st.write("""
This fraud detection system uses the Isolation Forest algorithm.

### How It Works:
Isolation Forest isolates anomalies instead of profiling normal data.
Fraudulent customers are identified based on unusual transaction behavior.

### Features Used:
- Transaction Amount
- Purchase Frequency
- Basket Value
- Risk Score

### Output:
- Anomaly = -1 → Fraud  
- Anomaly = 1 → Normal  
""")

st.markdown("---")

# ------------------ PREDICTION SECTION ------------------

st.subheader("🔮 Predict Customer Risk")

amount = st.number_input("Transaction Amount", min_value=0)
frequency = st.number_input("Purchase Frequency", min_value=0)
basket = st.number_input("Basket Value", min_value=0)

if st.button("Check Risk"):
    score = (amount * 0.3 + frequency * 0.3 + basket * 0.4)

    if score > 500:
        st.error("⚠️ High Risk Customer")
    elif score > 200:
        st.warning("⚠️ Medium Risk Customer")
    else:
        st.success("✅ Low Risk Customer")

st.markdown("---")

# ------------------ BUSINESS IMPACT ------------------

st.subheader("💼 Business Impact")

st.write("""
- Helps detect fraudulent transactions early  
- Reduces financial loss  
- Improves customer trust  
- Supports real-time monitoring  
""")