import requests
import pandas as pd
import os

def fetch_spacex_launch_data(api_url="https://api.spacexdata.com/v4/launches"):
    """
    Fetches all historical launch data from the SpaceX API v4.

    Args:
        api_url (str): The URL of the SpaceX launches API endpoint.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the fetched launch data.
                      Returns None if the request fails.
    """
    print(f"Fetching data from {api_url}...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print("Data fetched successfully.")
        # pd.json_normalize flattens the nested JSON structure
        return pd.json_normalize(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_data_as_json(dataframe, path, filename):
    """
    Saves a pandas DataFrame to a specified path as a JSON file.

    Args:
        dataframe (pd.DataFrame): The DataFrame to save.
        path (str): The directory path to save the file in.
        filename (str): The name of the file.
    """
    if dataframe is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = os.path.join(path, filename)
        dataframe.to_json(filepath, orient='records', indent=4)
        print(f"Data saved to {filepath}")
    else:
        print("No data to save.")

if __name__ == '__main__':
    # This block runs when the script is executed directly from the command line
    DATA_PATH = 'data/raw'
    FILENAME = 'spacex_api_data.json'
    
    launch_data = fetch_spacex_launch_data()
    save_data_as_json(launch_data, DATA_PATH, FILENAME)