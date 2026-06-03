import requests
from bs4 import BeautifulSoup
import os

# URLs to crawl
urls_to_scrape = [
    "http://www.dezykode.com/",
    "http://www.dezykode.com/courses/",
    "http://www.dezykode.com/internship/",
    "http://www.dezykode.com/about/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_scraped_text(text_list):
    seen = set()
    cleaned = []
    for line in text_list:
        line = line.strip()
        # Skip empty lines, typical headers/footers, navigation links, or duplicate phrases
        if not line or len(line) < 15 or "Subscribe Now" in line or line in seen:
            continue
        seen.add(line)
        cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    print("Starting crawl of DezyKode website...")
    all_knowledge = []
    
    for url in urls_to_scrape:
        try:
            print(f"Scraping data from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extract text specifically from page content tags
                for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
                    all_knowledge.append(tag.get_text())
            else:
                print(f"Failed to access page: Status code {response.status_code}")
        except Exception as e:
            print(f"Error accessing {url}: {e}")
            
    # Process and save collected strings
    processed_knowledge = clean_scraped_text(all_knowledge)
    
    with open("website_knowledge.txt", "w", encoding="utf-8") as file:
        file.write(processed_knowledge)
        
    print("\nSuccess! Generated 'website_knowledge.txt' containing your extracted dataset.")

if __name__ == "__main__":
    run_scraper()