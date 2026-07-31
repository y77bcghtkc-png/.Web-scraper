import csv
import time
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
class HNWContactScraper:
    def __init__(self):
        # User-agent rotation to mimic real browser traffic and prevent immediate blocking
        self.headers_list = [
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
                "Accept-Language": "en-US,en;q=0.5",
            }
        ]
    def build_search_queries(self):
        """
        Define targeted search queries focused on high-net-worth and wealth management sectors.
        """
        roles = [
            "Private Wealth Manager", 
            "Family Office Director", 
            "Private Banker", 
            "High Net Worth Advisor"
        ]
        
        # You can append locations or specific target parameters
        locations = ["New York", "London", "Geneva", "Singapore"]
        
        queries = []
        for role in roles:
            for location in locations:
                query = f"{role} {location} contact email profile"
                queries.append(query)
        return queries
    def fetch_search_results(self, query):
        """
        Simulates gathering public directory footprints or search snippets.
        Using a mock structure for safety, or querying public search endpoints.
        """
        formatted_query = query.replace(" ", "+")
        # Example target structure pointing to a search results page
        url = f"https://html.duckduckgo.com/html/?q={formatted_query}"
        
        headers = random.choice(self.headers_list)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"Error fetching query '{query}': {e}")
        return None
    def parse_contacts(self, html_content):
        """
        Parses HTML response to extract relevant professional links, titles, and snippets.
        """
        extracted_data = []
        if not html_content:
            return extracted_data
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # DuckDuckGo HTML layout selectors (adjust selectors based on target site choice)
        results = soup.find_all('div', class_='result')
        
        for result in results:
            title_tag = result.find('a', class_='result__snippet')
            header_tag = result.find('a', class_='result__title')
            
            if header_tag:
                title_text = header_tag.get_text(strip=True)
                link = header_tag.get('href', '')
                snippet_text = title_tag.get_text(strip=True) if title_tag else ""
                
                extracted_data.append({
                    "Title/Snippet": title_text,
                    "Company/Context": snippet_text,
                    "Source Link": link
                })
                
        return extracted_data
    def run_scraper(self, output_filename="hnw_b2b_contacts.csv"):
        queries = self.build_search_queries()
        all_contacts = []
        print(f"[*] Starting scraper across {len(queries)} targeted HNW sector footprints...")
        
        for query in queries:
            print(f"[*] Scraping data for query: {query}")
            html = self.fetch_search_results(query)
            
            if html:
                contacts = self.parse_contacts(html)
                all_contacts.extend(contacts)
            
            # Random delay to stay polite and avoid getting IP-blocked
            sleep_time = random.uniform(3.0, 7.0)
            time.sleep(sleep_time)
        # Convert to DataFrame and Export to CSV
        if all_contacts:
            df = pd.DataFrame(all_contacts)
            # Drop exact duplicates if any occur
            df.drop_duplicates(subset=["Source Link"], inplace=True)
            df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"[+] Success! Extracted {len(df)} unique records. Saved to {output_filename}")
        else:
            print("[-] No records extracted. Check network connection or selector configuration.")
if __name__ == "__main__":
    scraper = HNWContactScraper()
    scraper.run_scraper()
    