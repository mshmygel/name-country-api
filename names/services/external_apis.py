import requests
from requests.exceptions import RequestException, Timeout, ConnectionError


def get_nationalize_data(name: str):
    """
    Get country probability data for a given name from nationalize.io API.
    Returns a list of country entries or None if request fails or returns no data.
    """
    try:
        response = requests.get(f"https://api.nationalize.io/?name={name}", timeout=5)
        if response.status_code != 200:
            return None
        return response.json().get("country")
    except (RequestException, Timeout, ConnectionError):
        return None


def get_country_details(code: str):
    """
    Get detailed country data by alpha-2 code from restcountries API.
    Returns a dictionary with country data or None if request fails.
    """
    try:
        response = requests.get(f"https://restcountries.com/v3.1/alpha/{code}", timeout=5)
        if response.status_code != 200:
            return None
        return response.json()[0]
    except (RequestException, Timeout, ConnectionError, IndexError, ValueError):
        return None
