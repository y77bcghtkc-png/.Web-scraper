import time
import random
import pandas as pd
from duckduckgo_search import DDGS
class LiveHNWScraper:
    def __init__(self):
        self.queries = [
            "Private Wealth Manager email contact London",
            "Family Office Director email contact Geneva",
            "Private Banker contact New York",
            "High Net Worth Advisor profile email"
        ]
    def search_live_web(self):
        collected_data = []
        print("[*] Connecting to live search to fetch HNW contacts...")
        
        with DDGS() as ddgs:
            for query in self.queries:
                print(f"[*] Querying: {query}")
                try:
                    results = list(ddgs.text(query, max_results=3))
                    for r in results:
                        title = r.get('title', 'N/A')
                        href = r.get('href', 'N/A')
                        body = r.get('body', 'N/A')
                        
                        email_found = "Check Profile"
                        if "@" in body:
                            words = body.split()
                            for w in words:
                                if "@" in w and "." in w:
                                    email_found = w.strip(".,;")
                                    break
                        collected_data.append({
                            "Name/Title": title,
                            "Contact/Email": email_found,
                            "Snippet Details": body,
                            "Profile Link": href
                        })
                except Exception as e:
                    print(f"[-] Error executing query '{query}': {e}")
                
                time.sleep(random.uniform(2.0, 4.0))
                
        return collected_data
    def run_scraper(self, output_filename="hnw_b2b_contacts.csv"):
        data = self.search_live_web()
        
        if data:
            df = pd.DataFrame(data)
            df.drop_duplicates(subset=["Profile Link"], inplace=True)
            df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"[+] Success! Extracted {len(df)} live records and saved to {output_filename}")
        else:
            fallback_df = pd.DataFrame([{
                "Name/Title": "Private Wealth Director",
                "Contact/Email": "contact@wealth-advisory-example.com",
                "Snippet Details": "Sample record fetched during strict network filtering.",
                "Profile Link": "https://example.com"
            }])
            fallback_df.to_csv(output_filename, index=False, encoding='utf-8')
            print("[-] Live search returned empty, wrote baseline sample record.")
if __name__ == "__main__":
    scraper = LiveHNWScraper()
    scraper.run_scraper()