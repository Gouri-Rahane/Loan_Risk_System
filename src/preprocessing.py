import pandas as pd
def load_data():
    df = pd.read_csv("data/loan_data.csv")
    return df

def encode_categorical(df):
    df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
    df['Married'] = df['Married'].map({'Yes': 1, 'No': 0})
    df['Education'] = df['Education'].map({'Graduate': 1, 'Not Graduate': 0})
    df['Self_Employed'] = df['Self_Employed'].map({'Yes': 1, 'No': 0})
    df['Property_Area'] = df['Property_Area'].map({'Urban': 2, 'Semiurban': 1, 'Rural': 0})
    
    return df

def select_features(df):
    features = [
        'ApplicantIncome',
        'LoanAmount',
        'Credit_History',
        'Education'
    ]
    
    X = df[features]
    y = df['Loan_Status'].map({'Y': 1, 'N': 0})
    
    return X, y

def handle_missing_values(df):
    df['LoanAmount'].fillna(df['LoanAmount'].mean(), inplace=True)
    df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)
    return df

def preprocess_data():
    df = load_data()
    
    df = handle_missing_values(df)
    df = encode_categorical(df)
    
    X, y = select_features(df)
    
    return X, y

if __name__ == "__main__":
    X, y = preprocess_data()
    
    print("Features:\n", X.head())
    print("\nTarget:\n", y.head())