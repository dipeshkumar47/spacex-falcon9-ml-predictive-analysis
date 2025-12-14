import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate_model(model, X_test, y_test):
    """
    Calculates classification metrics for a given model on a test set.

    Args:
        model: A trained scikit-learn classifier.
        X_test: Test features.
        y_test: True labels for the test set.

    Returns:
        dict: A dictionary containing the accuracy, precision, recall, and f1-score.
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1-Score': f1_score(y_test, y_pred)
    }
    
    return metrics

def plot_confusion_matrix(y_test, y_pred, model_name):
    """
    Plots a confusion matrix for the given true and predicted labels.

    Args:
        y_test: True labels.
        y_pred: Predicted labels.
        model_name (str): The name of the model for the plot title.
    """
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Predicted Failure', 'Predicted Success'],
                yticklabels=['Actual Failure', 'Actual Success'])
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title(f'Confusion Matrix for {model_name}')
    plt.show()