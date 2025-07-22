# app/model_api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import pickle
import uvicorn
import io
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models')

with open(os.path.join(MODEL_PATH, 'final_classification_model.pkl'), 'rb') as f:
    clf_model = pickle.load(f)

with open(os.path.join(MODEL_PATH, 'final_regression_model.pkl'), 'rb') as f:
    reg_model = pickle.load(f)

with open(os.path.join(MODEL_PATH, 'final_cluster_model.pkl'), 'rb') as f:
    cluster_model = pickle.load(f)

app = FastAPI(title="Service Predictor API", version="1.0")

@app.get("/")
def root():
    return {"message": "Service ML Model API is 🔥 Running!"}

@app.post("/predict/classification")
async def classify(file: UploadFile = File(...)):
    data = await file.read()
    df = pd.read_csv(io.BytesIO(data))
    preds = clf_model.predict(df)
    df['classification_output'] = preds.tolist()
    return JSONResponse(content=df[['classification_output']].to_dict(orient="records"))

@app.post("/predict/regression")
async def regress(file: UploadFile = File(...)):
    data = await file.read()
    df = pd.read_csv(io.BytesIO(data))
    preds = reg_model.predict(df)
    df['regression_output'] = preds.tolist()
    return JSONResponse(content=df[['regression_output']].to_dict(orient="records"))

@app.post("/predict/clustering")
async def cluster(file: UploadFile = File(...)):
    data = await file.read()
    df = pd.read_csv(io.BytesIO(data))
    clusters = cluster_model.predict(df)
    df['cluster_output'] = clusters.tolist()
    return JSONResponse(content=df[['cluster_output']].to_dict(orient="records"))

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
