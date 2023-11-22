import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


class XMLSitemapExtractor:
    """Extract URLs from XML sitemaps of a given website."""

    def __init__(self, website_url):
        self.website_url = website_url
        self.extracted_dataframes = {}
        self.process_all_sitemaps()

    def retrieve_content(self, url):
        """Retrieve content from the specified URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as error:
            print(f"Error occurred while fetching URL content: {error}")
            return None

    def process_sitemap(self, sitemap_url):
        """Process an individual sitemap URL."""
        content = self.retrieve_content(sitemap_url)
        if content:
            soup = BeautifulSoup(content, "xml")
            links = [location.text for location in soup.find_all("loc")]
            dataframe_key = sitemap_url.split("/")[-1].replace(".xml", "")
            self.extracted_dataframes[dataframe_key] = self.create_dataframe(links)

    def process_all_sitemaps(self):
        """Retrieve and process all sitemaps found in the website's robots.txt."""
        robots_content = self.retrieve_content(f"{self.website_url}/robots.txt")
        if robots_content:
            for line in robots_content.decode("utf-8").split("\n"):
                if line.startswith("Sitemap:"):
                    self.process_sitemap(line.split(": ")[1].strip())

    def create_dataframe(self, url_list):
        """Convert a list of URLs into a DataFrame."""
        df = pd.DataFrame(url_list, columns=["ExtractedURLs"])
        return self.split_url_parts(df)

    def split_url_parts(self, dataframe):
        """Split URLs into components and add them as separate columns."""
        max_depth = 0
        for i, url in enumerate(dataframe["ExtractedURLs"]):
            parts = url.replace(self.website_url, "").strip("/").split("/")
            max_depth = max(max_depth, len(parts))
            for j, part in enumerate(parts):
                dataframe.at[i, f"Subdir_{j+1}"] = part
        for k in range(max_depth):
            if f"Subdir_{k+1}" not in dataframe.columns:
                dataframe[f"Subdir_{k+1}"] = None
        return dataframe

    def save_to_csv(self, directory="extracted_sitemaps"):
        """Save the extracted data to CSV files."""
        if not os.path.exists(directory):
            os.makedirs(directory)
        for key, df in self.extracted_dataframes.items():
            file_path = os.path.join(directory, f"{key}.csv")
            df.to_csv(file_path, index=False)


# Example usage
# extractor = XMLSitemapExtractor("https://www.example.com")
# extractor.save_to_csv()
