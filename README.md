# 🏦 Loan Risk Prediction System

An industry-level machine learning project to predict loan approval using applicant data.

## 🚀 Features

* 📊 Loan approval prediction (ML model)
* 🔥 Risk score calculation
* 🧠 Explainable AI (SHAP)
* 💻 Streamlit dashboard (premium UI)
* ⚡ FastAPI backend (REST API)
* 📈 Interactive charts & analytics

## 🛠 Tech Stack

* Python
* Scikit-learn
* Streamlit
* FastAPI
* Pandas, NumPy

## 📂 Project Structure

```
loan-risk-system/
├── app/          # Streamlit UI
├── src/          # ML logic
├── models/       # Trained model
├── data/         # Dataset
├── api.py        # FastAPI backend
```

## ▶️ Run Locally

### 1. Activate environment

```
venv\Scripts\activate
```

### 2. Run API

```
uvicorn api:app --reload
```

### 3. Run UI

```
streamlit run app/app.py
```

## 📊 Example

* Input: High income + good credit → Approved
* Input: Low income + bad credit → Rejected

---

## 🌟 Author

Gouri Rahane
