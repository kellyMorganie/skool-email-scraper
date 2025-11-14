thonpython
import re
import logging
import requests
from bs4 import BeautifulSoup

from .utilities import clean_email

class SkoolParser:
    BASE_URL = "https://skool.com/search?q="

    def __init__(self, proxies=None, domains=None):
        self.proxies = proxies
        self.domains = domains or []

    def search(self, keyword, location=None):
        query = keyword
        if location:
            query += f" {location}"

        url = self.BASE_URL + requests.utils.quote(query)
        logging.info(f"Fetching: {url}")

        try:
            response = requests.get(url, proxies=self.proxies, timeout=10)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Request failed: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        listings = soup.find_all("div", class_="listing")
        for item in listings:
            title = item.find("h2").get_text(strip=True) if item.find("h2") else "Unknown"
            description = item.find("p").get_text(strip=True) if item.find("p") else ""
            link = item.find("a")["href"] if item.find("a") else None

            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", description)
            for email in emails:
                email = clean_email(email)

                if self.domains and not any(email.endswith(d) for d in self.domains):
                    continue

                results.append({
                    "keyword": keyword,
                    "title": title,
                    "description": description,
                    "url": link,
                    "email": email
                })

        return results