{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "db4159a1-cce9-493e-9119-56c8d08da760",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import pandas as pd\n",
    "import os\n",
    "\n",
    "def fetch_spacex_launch_data(api_url = \"https://api.spacexdata.com/v4/launches\"):\n",
    "    ''' \n",
    "        Fetches all historical launch data from the SpaceX API v4.\n",
    "\n",
    "    Args:\n",
    "        api_url (str): The URL of the SpaceX launches API endpoint.\n",
    "\n",
    "    Returns:\n",
    "        pd.DataFrame: A pandas DataFrame containing the fetched launch data.\n",
    "                      Returns None if the request fails.\n",
    "    '''\n",
    "\n",
    "     print(f\"Fetching data from {api_url}...\")\n",
    "    try:\n",
    "        response = requests.get(api_url)\n",
    "        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)\n",
    "        print(\"Data fetched successfully.\")\n",
    "        # pd.json_normalize flattens the nested JSON structure\n",
    "        return pd.json_normalize(response.json())\n",
    "    except requests.exceptions.RequestException as e:\n",
    "        print(f\"Error fetching data: {e}\")\n",
    "        return None\n",
    "\n",
    "\n",
    "def save_data_as_json(dataframe, path, filename):\n",
    "    \"\"\"\n",
    "    Saves a pandas DataFrame to a specified path as a JSON file.\n",
    "\n",
    "    Args:\n",
    "        dataframe (pd.DataFrame): The DataFrame to save.\n",
    "        path (str): The directory path to save the file in.\n",
    "        filename (str): The name of the file.\n",
    "    \"\"\"\n",
    "    if dataframe is not None:\n",
    "        if not os.path.exists(path):\n",
    "            os.makedirs(path)\n",
    "        filepath = os.path.join(path, filename)\n",
    "        dataframe.to_json(filepath, orient='records', indent=4)\n",
    "        print(f\"Data saved to {filepath}\")\n",
    "    else:\n",
    "        print(\"No data to save.\")\n",
    "\n",
    "\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    # This block runs when the script is executed directly from the command line\n",
    "    DATA_PATH = 'data/raw'\n",
    "    FILENAME = 'spacex_api_data.json'\n",
    "    \n",
    "    launch_data = fetch_spacex_launch_data()\n",
    "    save_data_as_json(launch_data, DATA_PATH, FILENAME)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
