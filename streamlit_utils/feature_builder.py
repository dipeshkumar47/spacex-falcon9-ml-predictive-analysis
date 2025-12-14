import pandas as pd


"""
    Recreates the exact feature engineering pipeline used during training.
    
    Steps:
    1. One-hot encode categorical columns
    2. Align columns with training feature set
    3. Fill missing columns with 0
    4. Ensure correct column order

    Args:
        input_df (pd.DataFrame): Raw user input dataframe
        reference_columns (list): Columns used during model training

    Returns:
        pd.DataFrame: Final feature matrix ready for scaler + model
    """
# --------------------------------------------------
# THIS FUNCTION MUST MATCH TRAINING LOGIC EXACTLY
# --------------------------------------------------


def build_features(input_df: pd.DataFrame, scaler) -> pd.DataFrame:
    """
    Build model-ready features aligned EXACTLY to scaler schema
    """

    df = input_df.copy()

    # Drop non-model columns if present
    non_model_cols = ["BoosterVersion", "Date", "Outcome"]
    df = df.drop(columns=[c for c in non_model_cols if c in df.columns])

    # One-hot encode ONLY true categorical columns
    df = pd.get_dummies(
        df,
        columns=["Orbit", "LaunchSiteName"],
        drop_first=False
    )

    # 🔒 FINAL AUTHORITY: SCALER FEATURE SCHEMA
    df = df.reindex(
        columns=scaler.feature_names_in_,
        fill_value=0
    )

    return df

