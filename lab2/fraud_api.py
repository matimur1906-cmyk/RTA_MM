from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI(title="Fraud Detection API")

with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

FEATURES = ['amount', 'is_electronics', 'tx_per_minute']

class Transaction(BaseModel):
    amount: float
    is_electronics: int
    tx_per_minute: int

@app.post("/score")
def score(tx: Transaction):
    X = pd.DataFrame(
        [[tx.amount, tx.is_electronics, tx.tx_per_minute]],
        columns=FEATURES
    )

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]

    return {
        "is_fraud": bool(pred),
        "fraud_probability": float(proba)
    }
@app.get("/health")
def health():
    return {"status": "ok"}