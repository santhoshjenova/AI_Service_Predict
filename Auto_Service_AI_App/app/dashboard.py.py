# app/dashboard.py

import streamlit as st
import pandas as pd
import pickle
import datetime

# Load classification model (pending_service model)
with open('models/final_classification_model.pkl', 'rb') as f:
    classifier = pickle.load(f)

# Load regression model (next_service_due_days model)
with open('models/final_regression_model.pkl', 'rb') as f:
    regressor = pickle.load(f)

# Load cluster model
with open('models/final_cluster_model.pkl', 'rb') as f:
    clusterer = pickle.load(f)

st.set_page_config(page_title="ServicePal Dashboard", layout="wide")
st.title("🔧 Customer Service Intelligence Dashboard")

uploaded_file = st.file_uploader("📥 Upload Customer Data", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Simplified: assuming file is preprocessed
    st.subheader("Preview of Uploaded Data ⬇")
    st.dataframe(df.head())

    st.subheader("📈 Model Inference")

    # --- Classification Prediction
    if st.button("🔍 Predict: Pending Service"):
        classification_result = classifier.predict(df)
        df['pending_service_prediction'] = classification_result
        st.success("Classification complete")
        st.write(df[['pending_service_prediction']])
    
    # --- Regression Prediction
    if st.button("📅 Predict: Next Service Due Days"):
        regression_result = regressor.predict(df)
        df['predicted_next_due_days'] = regression_result
        st.success("Regression complete")
        st.write(df[['predicted_next_due_days']])
    
    # --- Clustering
    if st.button("🧠 Segment Customers (Clustering)"):
        cluster_labels = clusterer.predict(df)
        df['customer_segment'] = cluster_labels
        st.success("Clustering complete")
        st.write(df[['customer_segment']])

    with st.expander("📤 Download Full Results"):
        st.download_button("Download CSV", df.to_csv(index=False), file_name="prediction_results.csv")
