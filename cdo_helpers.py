import requests
from enum import Enum

# Define the valid timeRange intervals for the CDO metrics api
TIME_INTERVALS = ["5m", "15m", "30m", "1h"]


def create_session(bearer_token: str) -> str:
    """Helper function to set the auth token and accept headers in the API request"""
    http_session = requests.Session()
    http_session.headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": f"Python-FTD-Metrics",
        "Authorization": f"Bearer {bearer_token}",
    }
    return http_session


def get(api_client: requests.session, url: str, path: str = None, query: dict = None):
    """Given the API endpoint, path, and query, return the json payload from the API"""
    uri = url if path is None else f"{url}/{path}"
    result = api_client.get(
        url=uri,
        params=query,
    )
    result.raise_for_status()
    if result.json():
        return result.json()
