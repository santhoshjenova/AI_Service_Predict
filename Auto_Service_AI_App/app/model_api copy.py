import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Auto Service Predictor", layout="wide")
st.title("🔧 Auto Service Prediction Dashboard")

model_type = st.selectbox("Select Prediction Type", ["Classification", "Regression", "Clustering"])

uploaded_file = st.file_uploader("📤 Upload CSV File", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("✅ Uploaded Data", df.head())

    if st.button("🚀 Predict"):
        endpoint = f"http://127.0.0.1:8000/predict/{model_type.lower()}"
        try:
            response = requests.post(endpoint, files={"file": uploaded_file})
            if response.status_code == 200:
                result = pd.DataFrame(response.json())
                st.success("✅ Prediction Success")
                st.write("📊 Prediction Output", result)
                st.download_button("⬇️ Download Result", result.to_csv(index=False), "predictions.csv", "text/csv")
            else:
                st.error(f"❌ Error: {response.status_code}")
        except Exception as e:
            st.error(f"🚨 Could not connect to FastAPI: {e}")
