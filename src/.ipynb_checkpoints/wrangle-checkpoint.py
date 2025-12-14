import pandas as pd
import numpy as np
import requests

def get_payload_details():
    """Makes a new API call to the /payloads endpoint to get a lookup table."""
    try:
        payloads_url = "https://api.spacexdata.com/v4/payloads"
        response = requests.get(payloads_url)
        response.raise_for_status()
        payloads_data = response.json()
        payload_map = {p['id']: {'mass_kg': p.get('mass_kg'), 'orbit': p.get('orbit')} for p in payloads_data}
        return payload_map
    except Exception:
        return {}

def get_launchpad_details():
    """
    Fetch launchpad ID → name + region mapping
    """
    try:
        url = "https://api.spacexdata.com/v4/launchpads"
        response = requests.get(url)
        response.raise_for_status()
        pads = response.json()

        pad_map = {
            p['id']: f"{p.get('name')} ({p.get('region')})"
            for p in pads
        }
        return pad_map
    except Exception:
        return {}


def clean_api_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Final, correct data cleaning function that saves the correct IDs.
    """
    launchpad_map = get_launchpad_details()
    data = df[['flight_number', 'name', 'date_utc', 'launchpad', 'payloads', 'cores']].copy()
    
    payload_map = get_payload_details()

    def get_core_info(x, key):
        if isinstance(x, list) and x and isinstance(x[0], dict): return x[0].get(key)
        return None

    def get_payload_info(p_ids, key):
        if payload_map and isinstance(p_ids, list) and p_ids:
            return payload_map.get(p_ids[0], {}).get(key)
        return None
    
   
    # # The 'launchpad' column is a dictionary. I need to extract the 'id' from it.
    # def get_launchpad_id(x):
    #     if isinstance(x, str):
    #         return x
    #     return None
    #      # Return None if it's not a dictionary
    
    # data['LaunchSite'] = data['launchpad'].apply(get_launchpad_id)


    # Keep launchpad ID for MAP
    data['LaunchSite'] = data['launchpad']

    # Human-readable launch site for ML & graphs
    data['LaunchSiteName'] = data['launchpad'].apply(lambda x: launchpad_map.get(x, 'Unknown') if isinstance(x, str) else 'Unknown')



    data['BoosterVersion'] = data['name']
    data['PayloadMass'] = data['payloads'].apply(lambda x: get_payload_info(x, 'mass_kg'))
    data['Orbit'] = data['payloads'].apply(lambda x: get_payload_info(x, 'orbit'))
    
    data['Outcome'] = data['cores'].apply(lambda x: get_core_info(x, 'landing_success'))
    data['Flights'] = data['cores'].apply(lambda x: get_core_info(x, 'flight'))
    data['GridFins'] = data['cores'].apply(lambda x: get_core_info(x, 'gridfins'))
    data['Reused'] = data['cores'].apply(lambda x: get_core_info(x, 'reused'))
    data['Legs'] = data['cores'].apply(lambda x: get_core_info(x, 'legs'))
    
    data['Date'] = pd.to_datetime(data['date_utc'], errors='coerce')
    data['class'] = data['Outcome'].apply(lambda x: 1 if x is True else 0)

    data = data.drop(columns=['cores', 'payloads', 'launchpad', 'date_utc', 'name'])

    mean_payload = data['PayloadMass'].mean()
    if pd.notna(mean_payload):
        data['PayloadMass'] = data['PayloadMass'].fillna(value=mean_payload)

    
    data = data.fillna({
        'Orbit': 'Unknown',
        'LaunchSite': 'Unknown',
        'Outcome': False,
        'Flights': 0,
        'GridFins': False,
        'Reused': False,
        'Legs': False
    })

    final_cols = [
    'flight_number', 'Date', 'BoosterVersion', 'PayloadMass',
    'Orbit', 'LaunchSite', 'LaunchSiteName',
    'Outcome', 'Flights', 'GridFins', 'Reused', 'Legs', 'class'
]

    
    return data[final_cols]