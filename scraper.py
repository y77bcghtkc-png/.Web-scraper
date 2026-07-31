import time
import random
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
                print(f"\n[*] Querying: {query}")
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
                            "Profile Link": href
                        })
                except Exception as e:
                    print(f"[-] Error executing query '{query}': {e}")
                
                time.sleep(random.uniform(2.0, 4.0))
                
        return collected_data
    def run_scraper(self):
        data = self.search_live_web()
        
        print("\n" + "="*50)
        print(f"EXTRACTED HNW CONTACT RESULTS ({len(data)} found):")
        print("="*50)
        for i, item in enumerate(data, 1):
            print(f"{i}. Title: {item['Name/Title']}")
            print(f"   Email: {item['Contact/Email']}")
            print(f"   Link:  {item['Profile Link']}")
            print("-" * 50)
if __name__ == "__main__":
    scraper = LiveHNWScraper()
    scraper.run_scraper()