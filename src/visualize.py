import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_feature_importance(model, feature_names):
    """
    Plots feature importances for tree-based models.

    Args:
        model: A trained scikit-learn model (e.g., RandomForest, DecisionTree).
        feature_names (list): A list of names for the features.
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        
        feature_importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        
        plt.figure(figsize=(12, 10))
        sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
        plt.title('Feature Importances')
        plt.show()
    else:
        print(f"The model {type(model).__name__} does not have 'feature_importances_'.")

def plot_success_rate_by_category(df, category_col):
    """
    Plots the landing success rate for a given categorical column.

    Args:
        df (pd.DataFrame): DataFrame containing the launch data.
        category_col (str): The name of the categorical column to group by.
    """
    success_rate_df = df.groupby(category_col)['class'].mean().reset_index().sort_values(by='class', ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='class', y=category_col, data=success_rate_df, orient='h')
    plt.title(f'Landing Success Rate by {category_col}')
    plt.xlabel('Success Rate')
    plt.ylabel(category_col)
    plt.show()