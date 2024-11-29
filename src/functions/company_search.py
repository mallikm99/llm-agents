import os

import requests

# Replace with your actual API key
API_KEY = os.environ.get('FINANCIAL_MODELING_PREP_API_KEY')

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

def general_search(query):
    """
    Search over 70,000 symbols by symbol name or company name, including cryptocurrencies, forex, stocks, ETFs, and other financial instruments.
    """
    url = f'https://financialmodelingprep.com/api/v3/search?query={query}&apikey={API_KEY}'
    return fetch_data(url)

def ticker_search(query, limit=10, exchange=''):
    """
    Find ticker symbols and exchanges for both equity securities and ETFs by searching with the company name or ticker symbol.
    """
    url = f'https://financialmodelingprep.com/api/v3/search-ticker?query={query}&limit={limit}&exchange={exchange}&apikey={API_KEY}'
    return fetch_data(url)

def name_search(query, limit=10, exchange=''):
    """
    Find ticker symbols and exchange information for equity securities and ETFs by searching with the company name.
    """
    url = f'https://financialmodelingprep.com/api/v3/search-name?query={query}&limit={limit}&exchange={exchange}&apikey={API_KEY}'
    return fetch_data(url)

def cik_name_search(query):
    """
    Discover CIK numbers for SEC-registered entities by company name.
    """
    url = f'https://financialmodelingprep.com/api/v3/cik-search/{query}?apikey={API_KEY}'
    return fetch_data(url)

def cik_search(cik):
    """
    Find registered company names linked to SEC-registered entities using their CIK Number.
    """
    url = f'https://financialmodelingprep.com/api/v3/cik/{cik}?apikey={API_KEY}'
    return fetch_data(url)

def cusip_search(cusip):
    """
    Access information about financial instruments and securities by entering their unique CUSIP numbers.
    """
    url = f'https://financialmodelingprep.com/api/v3/cusip/{cusip}?apikey={API_KEY}'
    return fetch_data(url)

def isin_search(isin):
    """
    Find information about financial instruments and securities by entering their unique ISIN.
    """
    url = f'https://financialmodelingprep.com/api/v4/search/isin?isin={isin}&apikey={API_KEY}'
    return fetch_data(url)
