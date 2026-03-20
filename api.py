from fastapi import FastAPI
import pickle
import numpy as np
import os

app = FastAPI()

# Load model safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

model = pickle.load(open(MODEL_PATH, "rb"))

@app.get("/")
def home():
    return {"message": "Loan Prediction API is running 🚀"}

@app.post("/predict")
def predict(income: float, loan_amount: float, credit_history: int):
    
    input_data = np.array([[income, loan_amount, credit_history]])
    
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    return {
        "prediction": int(prediction),
        "risk_score": round(float(prob)*100, 2)
    }