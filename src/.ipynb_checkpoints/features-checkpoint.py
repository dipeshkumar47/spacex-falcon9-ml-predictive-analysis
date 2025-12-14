import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def create_features(df):
    """
    Performs one-hot encoding on categorical features of the launch data.

    Args:
        df (pd.DataFrame): The cleaned launch data DataFrame.

    Returns:
        pd.DataFrame: DataFrame with categorical features one-hot encoded.
    """

    # Categorical columns for ML
    features_to_encode = ['Orbit', 'LaunchSiteName', 'GridFins', 'Reused', 'Legs']
    
    # One-hot encode
    features_one_hot = pd.get_dummies(df[features_to_encode])
    
    # Drop original categorical + ID column
    df = df.drop(columns=features_to_encode + ['LaunchSite'])
    
    # Combine
    df = pd.concat([df, features_one_hot], axis=1)
    
    return df


def split_and_scale_data(X, Y, test_size=0.2, random_state=42):
    """
    Splits the feature and target data into training and testing sets
    and applies standard scaling to the feature sets.

    Args:
        X (pd.DataFrame): The feature matrix.
        Y (pd.Series or np.array): The target vector.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int): The seed used by the random number generator.

    Returns:
        tuple: A tuple containing X_train, X_test, Y_train, Y_test, and the fitted scaler object.
    """
    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=random_state)
    
    # Initialize the StandardScaler
    scaler = StandardScaler()
    
    # Fit the scaler on the training data and transform it
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Transform the test data using the same fitted scaler
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, Y_train, Y_test, scaler