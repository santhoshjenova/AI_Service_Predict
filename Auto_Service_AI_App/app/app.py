# app/model_api.py
!pip install fastapi

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import pickle
import uvicorn
import io

# Load models
with open('models/final_classification_model.pkl', 'rb') as f:
    clf_model = pickle.load(f)

with open('models/final_regression_model.pkl', 'rb') as f:
    reg_model = pickle.load(f)

with open('models/final_cluster_model.pkl', 'rb') as f:
    cluster_model = pickle.load(f)

app = FastAPI(title="Service Predictor API", version="1.0")

@app.get("/")
def root():
    return {"message": "Service ML Model API is 🔥 Running!"}

@app.post("/predict/classification")
def classify(file: UploadFile = File(...)):
    df = pd.read_csv(io.BytesIO(file.file.read()))
    preds = clf_model.predict(df)
    df['classification_output'] = preds.tolist()
    return JSONResponse(content=df[['classification_output']].to_dict(orient="records"))

@app.post("/predict/regression")
def regress(file: UploadFile = File(...)):
    df = pd.read_csv(io.BytesIO(file.file.read()))
    preds = reg_model.predict(df)
    df['regression_output'] = preds.tolist()
    return JSONResponse(content=df[['regression_output']].to_dict(orient="records"))

@app.post("/predict/clustering")
def cluster(file: UploadFile = File(...)):
    df = pd.read_csv(io.BytesIO(file.file.read()))
    clusters = cluster_model.predict(df)
    df['cluster_output'] = clusters.tolist()
    return JSONResponse(content=df[['cluster_output']].to_dict(orient="records"))

# Run locally with: python model_api.py
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
