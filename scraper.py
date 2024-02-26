import json
import csv
import sys
from typing import Any, Dict
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data(ticker_symbol: Any) -> Dict[str, Any]:
    """
    Get stock data for a given ticker symbol from Yahoo Finance.
    Parameters:
    - ticker_symbol (Any): Ticker symbol of the stock.
    Returns:
    - Dict[str, Any]: Dictionary containing stock data.
    """
    print('Getting stock data of ', ticker_symbol)

    # Set user agent to avoid detection as a scraper
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

    # Construct URL for the given ticker_symbol
    url = f'https://finance.yahoo.com/quote/{ticker_symbol}'
    # Make a request to the URL
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # description_element = soup.find('section', {'class': 'quote-sub-section'})
    # description_paragraph = description_element.find('p', {'class': 'Mt(15px) Lh(1.6)'}) if description_element else None
    # description = description_paragraph.text.strip() if description_paragraph else ''
    # Extract stock data from the HTML
    stock = {
    # scraping the stock data from the price indicators
    'stock_name': soup.find('div', {'class':'D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find_all('div')[0].text.strip(),
    'regularMarketPrice': soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text.strip(),
    'regularMarketChange': soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text.strip(),
    'regularMarketChangePercent': soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text.strip(),
    'quote': soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('span')[2].text.strip(),

    # scraping the stock data from the "Summary" table
    'previous_close': soup.find('table', {'class':'W(100%)'}).find_all('td')[1].text.strip(),
    'open_value': soup.find('table', {'class':'W(100%)'}).find_all('td')[3].text.strip(),
    'bid': soup.find('table', {'class':'W(100%)'}).find_all('td')[5].text.strip(),
    'ask': soup.find('table', {'class':'W(100%)'}).find_all('td')[7].text.strip(),
    'days_range': soup.find('table', {'class':'W(100%)'}).find_all('td')[9].text.strip(),
    'week_range': soup.find('table', {'class':'W(100%)'}).find_all('td')[11].text.strip(),
    'volume': soup.find('table', {'class':'W(100%)'}).find_all('td')[13].text.strip(),
    'avg_volume': soup.find('table', {'class':'W(100%)'}).find_all('td')[5].text.strip(),
    'market_cap': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[1].text.strip(),
    'beta': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[3].text.strip(),
    'pe_ratio': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[5].text.strip(),
    'eps': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[7].text.strip(),
    'earnings_date': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[9].text.strip(),
    'dividend_yield': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[11].text.strip(),
    'ex_dividend_date': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[13].text.strip(),
    'year_target_est': soup.find('table', {'class':'W(100%) M(0) Bdcl(c)'}).find_all('td')[15].text.strip(),
    }
    return stock

# Check if ticker symbols are provided as command line arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <ticker_symbol1> <ticker_symbol2> ...")
    sys.exit(1)

# Extract ticker symbols from command line arguments
ticker_symbols = sys.argv[1:]

# Get stock data for each ticker symbol
stockdata = [get_data(symbol) for symbol in ticker_symbols]

# Writing stock data to a JSON file
with open('stock_data.json', 'w', encoding='utf-8') as f:
    json.dump(stockdata, f)

# Writing stock data to a CSV file with aligned values
CSV_FILE_PATH = 'stock_data.csv'
with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = stockdata[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(stockdata)

# Writing stock data to an Excel file
EXCEL_FILE_PATH = 'stock_data.xlsx'
df = pd.DataFrame(stockdata)
df.to_excel(EXCEL_FILE_PATH, index=False)

print('Done!')
