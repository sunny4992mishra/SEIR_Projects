import requests
from bs4 import BeautifulSoup
import sys

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

if __name__ == "__main__":
    
    if len(sys.argv)==2:
        url=sys.argv[1]
        result=read_url(url)
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