import requests
import csv
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/quote/AAPL/history/?period1=1420070400&period2=1750040863"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

response = requests.get(url, headers=headers, timeout=10)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    historical_table = soup.find('table')
    if historical_table:
        tbody = historical_table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            with open('AAPL.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        writer.writerow([col.text.strip() for col in cols[:7]])
            print(f"Saved {len(rows)} rows to 'AAPL.csv'.")
        else:
            print("No table body found.")
    else:
        print("No table found.")
else:
    print(f"Failed to fetch page: {response.status_code}")
