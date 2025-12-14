import os
import joblib
import pandas as pd

# --------------------------------------------------
# BASE PROJECT DIRECTORY
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
# -> spacex-ml-project/

# --------------------------------------------------
# LOAD MODEL & SCALER
# --------------------------------------------------
def load_model_and_scaler():
    model_path = os.path.join(BASE_DIR, "models", "best_model.pkl")
    scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    return model, scaler


# --------------------------------------------------
# GET TRAINING FEATURE COLUMNS
# --------------------------------------------------
def get_training_columns():
    """
    Reads processed training CSV to extract feature column order
    """
    data_path = os.path.join(
        BASE_DIR, "data", "processed", "processed_for_training.csv"
    )

    df = pd.read_csv(data_path)

    target = "class"
    feature_columns = df.drop(columns=[target]).columns.tolist()

    return feature_columns
