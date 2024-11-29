import requests
import os

# Replace with your actual API key
API_KEY = os.environ.get('FINANCIAL_MODELING_PREP_API_KEY')

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

def get_all_stocks():
    """
    Retrieve a comprehensive list of all traded and non-traded stocks.
    """
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}'
    return fetch_data(url)

def get_etf_list():
    """
    Retrieve a list of all Exchange Traded Funds (ETFs).
    """
    url = f'https://financialmodelingprep.com/api/v3/etf/list?apikey={API_KEY}'
    return fetch_data(url)

def get_financial_statement_symbols():
    """
    Retrieve a list of all companies with available financial statements.
    """
    url = f'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={API_KEY}'
    return fetch_data(url)

def get_tradable_stocks():
    """
    Retrieve a list of all actively traded stocks.
    """
    url = f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={API_KEY}'
    return fetch_data(url)

def get_commitment_of_traders_report():
    """
    Retrieve the Commitment of Traders Report.
    """
    url = f'https://financialmodelingprep.com/api/v4/commitment_of_traders_report/list?apikey={API_KEY}'
    return fetch_data(url)

def get_cik_list():
    """
    Retrieve a comprehensive list of 13F CIK numbers for SEC-registered entities.
    """
    url = f'https://financialmodelingprep.com/api/v3/cik_list?apikey={API_KEY}'
    return fetch_data(url)

def get_euronext_symbols():
    """
    Retrieve all symbols for stocks traded on Euronext exchanges.
    """
    url = f'https://financialmodelingprep.com/api/v3/symbol/available-euronext?apikey={API_KEY}'
    return fetch_data(url)

def get_symbol_changes():
    """
    Retrieve the latest symbol changes due to mergers, acquisitions, stock splits, and name changes.
    """
    url = f'https://financialmodelingprep.com/api/v4/symbol_change?apikey={API_KEY}'
    return fetch_data(url)

def get_exchange_symbols(exchange):
    """
    Retrieve all symbols for a given exchange.
    """
    url = f'https://financialmodelingprep.com/api/v3/symbol/{exchange}?apikey={API_KEY}'
    return fetch_data(url)

def get_available_indexes():
    """
    Retrieve a list of all available indexes.
    """
    url = f'https://financialmodelingprep.com/api/v3/symbol/available-indexes?apikey={API_KEY}'
    return fetch_data(url)
