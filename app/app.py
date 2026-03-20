import streamlit as st
import numpy as np
import requests
import pandas as pd
import json

# Page config
st.set_page_config(
    page_title="Loan Risk System",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>

/* 🌙 Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #ffffff;
}

/* 🧊 Glass card */
.glass {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* 🔤 Fix ALL text visibility */
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #f1f5f9 !important;
}

/* 📊 Tabs text */
button[data-baseweb="tab"] {
    color: #e2e8f0 !important;
    font-weight: 600;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
}

/* Input fields */
input, select {
    color: black !important;
    background-color: rgba(255,255,255,0.1) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    color: #ffffff;
}

/* Chart text fix */
svg text {
    fill: white !important;
}

/* Buttons */
button[kind="primary"] {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 10px;
}

/* Fix Streamlit buttons visibility */
button {
    color: black !important;
    font-weight: 600;
}

/* Primary button (Predict) */
button[kind="primary"] {
    background-color: #3b82f6 !important;
    color: white !important;
}

/* Download button fix */
[data-testid="stDownloadButton"] button {
    background-color: #10b981 !important;
    color: white !important;
    border-radius: 10px;
}

/* Fix white containers (charts area) */
[data-testid="stVerticalBlock"] {
    color: #ffffff !important;
}

/* Fix labels inside white chart area */
svg text {
    fill: black !important;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="glass">
    <h1 style='text-align: center; color: #60a5fa;'>
    🏦 Loan Approval Dashboard
    </h1>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Loan Risk System")
st.sidebar.write("Enter applicant details")

# API Status
try:
    requests.get("http://127.0.0.1:8000")
    st.sidebar.success("API Connected ✅")
except:
    st.sidebar.error("API Not Connected ❌")

# Inputs
income = st.sidebar.number_input("Applicant Income", min_value=0.0)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=0.0)

credit_history = st.sidebar.selectbox(
    "Credit History",
    [1, 0],
    format_func=lambda x: "Good (1)" if x == 1 else "Bad (0)"
)

# Tabs
tab1, tab2 = st.tabs(["Prediction", "Analytics"])

# ------------------ TAB 1 ------------------
with tab1:

    # Metrics
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("Income", income)
    col2.metric("Loan Amount", loan_amount)
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    # Chart
    chart_data = pd.DataFrame({
        "Feature": ["Income", "Loan Amount", "Credit History"],
        "Value": [income, loan_amount, credit_history]
    })

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.bar_chart(chart_data.set_index("Feature"), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # API URL
    API_URL = "http://127.0.0.1:8000/predict"

    # Validation
    valid_input = True
    if income <= 0 or loan_amount <= 0:
        st.warning("Please enter valid positive values")
        valid_input = False

    # Prediction
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    if st.button("Predict"):

        if not valid_input:
            st.stop()

        payload = {
            "income": income,
            "loan_amount": loan_amount,
            "credit_history": credit_history
        }

        with st.spinner("Analyzing application..."):
            response = requests.post(API_URL, params=payload)

        if response.status_code == 200:
            result = response.json()

            prediction = result["prediction"]
            risk_score = result["risk_score"] / 100

            # Result
            if prediction == 1:
                st.success("Loan Approved ✅")
            else:
                st.error("Loan Rejected ❌")

            # Explanation
            if credit_history == 1:
                st.info("Good credit history increases approval chances ✅")
            else:
                st.warning("Poor credit history reduces approval chances ❌")

            # Risk Score
            st.subheader("Risk Score")
            st.write(f"{risk_score*100:.2f}% chance of approval")

            # Risk Level
            if risk_score > 0.75:
                st.success("Low Risk 🟢")
            elif risk_score > 0.4:
                st.warning("Medium Risk 🟡")
            else:
                st.error("High Risk 🔴")

            # -------- Prediction History --------
            if "history" not in st.session_state:
                st.session_state.history = []

            st.session_state.history.append({
                "Income": income,
                "Loan": loan_amount,
                "Result": "Approved" if prediction == 1 else "Rejected"
            })

            st.subheader("Prediction History")
            st.table(st.session_state.history)

            # -------- Download Report --------
            report = {
                "income": income,
                "loan_amount": loan_amount,
                "prediction": prediction,
                "risk_score": risk_score
            }

            st.download_button(
                label="Download Report",
                data=json.dumps(report),
                file_name="loan_report.json",
                mime="application/json"
            )

        else:
            st.error("API Error ❌")
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------ TAB 2 ------------------
with tab2:
    st.subheader("📊 Business Insights")

    st.markdown("""
    - High income + good credit → approval likely  
    - Low income + bad credit → rejection likely  
    - Credit history is the most important factor  
    """)