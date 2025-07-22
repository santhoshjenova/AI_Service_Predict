# utils/preprocessing.py

import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler

def preprocess_input(df: pd.DataFrame, scaler: StandardScaler, drop_columns: list = None) -> pd.DataFrame:
    """
    Clean, transform, and scale the input features for prediction.

    Args:
        df (pd.DataFrame): Raw input data.
        scaler (StandardScaler): Pre-fitted or preloaded scaler object.
        drop_columns (list): List of columns to drop.

    Returns:
        pd.DataFrame: Cleaned and scaled data ready for model prediction.
    """

    df = df.copy()

    # Handle date columns
    if 'last_service_date' in df.columns:
        df['last_service_date'] = pd.to_datetime(df['last_service_date'], errors='coerce')
        df['days_since_last_service'] = (datetime.today() - df['last_service_date']).dt.days
        df.drop(columns=['last_service_date'], inplace=True)

    # Drop unwanted columns
    if drop_columns:
        df.drop(columns=[col for col in drop_columns if col in df.columns], inplace=True, errors='ignore')

    # Handle categorical features if needed
    df = pd.get_dummies(df)

    # Handle any NaNs
    df.fillna(0, inplace=True)

    # Scale features
    X_scaled = scaler.transform(df)

    return X_scaled
