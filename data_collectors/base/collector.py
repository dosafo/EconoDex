import os
import json
import requests
BLS_API_KEY  = os.environ.get('BLS_API_KEY')
BLS_ENDPOINT = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
def fetch_bls_series(series, **kwargs):
    """
    Pass in a list of BLS timeseries to fetch data and return the series
    in JSON format. Arguments can also be provided as kwargs:
        - startyear (4 digit year)
        - endyear (4 digit year)
        - catalog (True or False)
        - calculations (True or False)
        - annualaverage (True or False)
        - registrationkey (api key from BLS website)
    If the registrationkey is not passed in, this function will use the
    BLS_API_KEY fetched from the environment.
    """
    if len(series) < 1 or len(series) > 25:
        raise ValueError("Must pass in between 1 and 25 series ids")
    # Create headers and payload post data
    headers = {'Content-Type': 'application/json'}
    payload = {
        'seriesid': series,
        'registrationkey': BLS_API_KEY,
    }
    # Update the payload with the keyword arguments
    payload.update(kwargs)
    # Fetch the response from the BLS API
    response = requests.post(BLS_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    # Parse the JSON result
    result = response.json()
    if result['status'] != 'REQUEST_SUCCEEDED':
        raise Exception(result['message'][0])
    print(result)
    return result
