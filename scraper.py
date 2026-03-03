import requests
from bs4 import BeautifulSoup
import sys,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def read_url(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
    }
    
    try:
        page=requests.get(url,headers=headers,timeout=10)
        page.raise_for_status()

        soup=BeautifulSoup(page.text,"lxml")
        title=soup.title.get_text(strip=True) if soup.title else "No title"
        body=soup.body.get_text(strip=True) if soup.body else "No body"
        links=[link['href'] for link in soup.find_all('a',href=True)]
        
        return {"title": title, "body": body, "links": links}

    except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")
            return None

def scrape_dynamic(url):
    result={}
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        
    except Exception as e:
        print(f"Failed to start browser: {e}")
        sys.exit(1)

    try:
        driver.get(url)
        time.sleep(1)

        result["title"]=driver.title
      
        result["body"]=driver.find_element("tag name", "body").text 
        
        links = []
        for a in driver.find_elements("tag name", "a"):
            href = a.get_attribute("href")
            if href:
                links.append(href)
        result["links"]=links
        return result

    except Exception as e:
        print(f"Scraping error: {e}")
        sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    
    if len(sys.argv)==2:
        url=sys.argv[1]
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        result=read_url(url)
        if len(result["body"])<50 or len(result["links"])==0:
            result=scrape_dynamic(url)
        if result:
            print("Title:", result["title"])
            print()
            print("Body: " , result["body"])
            print()
            print("Links found:", len(result["links"]))
            print()
            for link in result["links"]:
                print(link)
    else:
        print("Invalid input")
        sys.exit(1)