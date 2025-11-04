import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def preprocess_data():
    df = pd.read_csv('Mall_Customers.csv')
    df_original = df.copy()  # Keep original for comparison

    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("\nMissing values found:")
        print(missing)
        print("\nOriginal data head:")
        print(df_original.head())
        print("\nData after handling missing values:")
        # Assuming no imputation, just drop or note
        print("(No imputation applied, proceeding)")

    # Check for duplicates
    duplicates = df[df.duplicated()]
    if len(duplicates) > 0:
        print(f"\n{len(duplicates)} duplicate rows found:")
        print(duplicates)
        print("\nOriginal data head:")
        print(df_original.head())

        # Data cleaning (drop duplicates)
        df = df.drop_duplicates()
        print("\nData after removing duplicates:")
        print(df.head())

    # Initial feature selection <------如果你做完visualization後要去掉不相干的特徵,在這邊修改
    df = df.drop(columns=['CustomerID'])  # Assuming CustomerID is not useful for analysis

    # Data preprocessing: OneHot encode categorical variable (Genre)
    ohe = OneHotEncoder(drop='first', sparse_output=False)  # drop='first' to avoid multicollinearity
    genre_encoded = ohe.fit_transform(df[['Genre']])
    genre_df = pd.DataFrame(genre_encoded, columns=ohe.get_feature_names_out(['Genre']))
    df = pd.concat([df.drop(columns=['Genre']), genre_df], axis=1)

    # Data preprocessing: Scale numerical features appropriately
    scaler = StandardScaler()
    numerical_cols = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    return df

if __name__ == '__main__':
    # Load and display original data
    df_original = pd.read_csv('Mall_Customers.csv')
    print("Original Dataset info (Schema):")
    df_original.info()
    print("\nOriginal Dataset head (First 5 rows):")
    print(df_original.head())

    df = preprocess_data()

    print("\nOneHot encoded Genre: Created Genre_Male (1 if Male, 0 otherwise)")
    print("Scaled numerical features using StandardScaler.")
    print("Processed dataset head (after preprocessing):")
    print(df.head())
