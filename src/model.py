import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data
df = pd.read_csv("data/loan_data.csv")

# Basic preprocessing (minimal for now)
df['LoanAmount'].fillna(df['LoanAmount'].mean(), inplace=True)
df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)


df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

# Features
X = df[['ApplicantIncome', 'LoanAmount', 'Credit_History']]
y = df['Loan_Status']

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
import os
os.makedirs("models", exist_ok=True)

with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved successfully!")