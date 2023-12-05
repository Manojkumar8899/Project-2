import requests
import pandas as pd


class OpenAQDataFetcher:
    """
    Fetches air quality data from the OpenAQ API.

    Attributes:
        url (str): The API endpoint URL.
        headers (dict): HTTP headers for the API request.
    """

    def __init__(self, url, headers):
        """
        Initializes the data fetcher with API URL and headers.

        Args:
            url (str): The API endpoint URL.
                Should include parameters such as date range, location, or any other necessary filters.
                Example: "https://api.openaq.org/v2/measurements?date_from=..."
            headers (dict): HTTP headers for the API request.
                Should include required headers such as API key, content type, etc.
                Example: {"X-API-Key": "...", 'accept': 'application/json', 'content-type': 'application/json'}
        """
        self.url = url
        self.headers = headers

    def fetch_data(self):
        """
        Fetches data from the OpenAQ API.

        Returns:
            list: A list of data points if the request is successful, None otherwise.
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.json()["results"]
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return None


# Usage example
# url = "https://api.openaq.org/v2/measurements?date_from=..."
# headers = {"X-API-Key": "...", 'accept': 'application/json', 'content-type': 'application/json'}
# data_fetcher = OpenAQDataFetcher(url, headers)
# data = data_fetcher.fetch_data()
# df = pd.DataFrame(data) if data else pd.DataFrame()
