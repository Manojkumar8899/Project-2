import requests
from bs4 import BeautifulSoup
import pandas as pd


class TheatreScraper:
    """
    A class to scrape theatre information from 'https://www.cinemaprofile.com'.

    Attributes:
        base_url (str): Base URL of the website to scrape.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get_soup_from_url(self, url):
        """
        Fetch and parse HTML content from a URL.

        Args:
            url (str): URL to fetch the content from.

        Returns:
            BeautifulSoup: Parsed HTML content of the page, or None if an error occurs.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Error during request to {url}: {e}")
            return None

    def fetch_content(self, url):
        """
        Fetch and parse HTML content from a URL.

        Args:
            url (str): URL to fetch the content from.

        Returns:
            BeautifulSoup: Parsed HTML content of the page, or None if an error occurs.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return None

    def extract_category_links(self, soup):
        """
        Extract category links from the main page content.

        Args:
            soup (BeautifulSoup): Parsed HTML content of the main page.

        Returns:
            list: List of category URLs.
        """
        category_div = soup.find_all("div", class_="lettersort")[1]
        return [
            self.base_url + a["href"] for a in category_div.find_all("a", href=True)
        ][2:]

    def append_pagination_links(self, initial_links):
        """
        Append pagination links to the initial category links list.

        Args:
            initial_links (list): Initial list of category links.

        Returns:
            list: Extended list of category links including pagination.
        """
        extended_links = initial_links.copy()
        for link in initial_links:
            soup = self.get_soup_from_url(link)
            if soup:
                pagination_div = soup.find("div", class_="cat-pagintn float-width")
                if pagination_div:
                    pagination_links = [
                        self.base_url + a["href"]
                        for a in pagination_div.find_all("a", href=True)
                        if "page=" in a["href"]
                    ][:-1]
                    extended_links.extend(pagination_links)
        return extended_links

    def extract_theatre_info(self, url):
        """
        Extract theatre information from a single page URL.

        Args:
            url (str): URL of the page to extract theatre information.

        Returns:
            list: List of dictionaries containing theatre information.
        """
        response = requests.get(url)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.content, "html.parser")
        theatres = soup.find_all("div", class_="pol-rt-sm float-width listshome")

        theatre_info = []
        for theatre in theatres:
            name_tag = theatre.find("h5")
            location_tag = theatre.find("h6")

            city, state = "N/A", "N/A"
            if location_tag:
                location_parts = location_tag.get_text(strip=True).split(",")
                city = location_parts[0].strip() if len(location_parts) > 0 else "N/A"
                state = location_parts[1].strip() if len(location_parts) > 1 else "N/A"

            theatre_data = {
                "Name": name_tag.get_text(strip=True) if name_tag else "N/A",
                "City": city,
                "State": state,
                "Details URL": name_tag.find("a")["href"]
                if name_tag and name_tag.find("a")
                else "N/A",
            }
            theatre_info.append(theatre_data)

        return theatre_info

    def scrape_theatres(self):
        """
        Scrape theatre information from the entire website.

        Returns:
            DataFrame: DataFrame containing all scraped theatre information.
        """
        main_page_soup = self.get_soup_from_url(
            self.base_url + "theatres-list-in-india.html"
        )
        if not main_page_soup:
            return pd.DataFrame()

        category_links = self.extract_category_links(main_page_soup)
        all_links = self.append_pagination_links(category_links)

        all_theatre_info = []
        for link in all_links:
            all_theatre_info.extend(self.extract_theatre_info(link))

        return pd.DataFrame(all_theatre_info)

    def save_to_csv(self, dataframe, filename):
        """
        Save the scraped theatre information to a CSV file.

        Args:
            dataframe (DataFrame): DataFrame containing the theatre information.
            filename (str): Filename for the CSV file.
        """
        dataframe.to_csv(filename, index=False)
