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

def get_company_profile(symbol):
    """
    Retrieve a comprehensive overview of a company, including price, beta, market capitalization, description, headquarters, and more.
    """
    url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={API_KEY}'
    return fetch_data(url)

def get_executive_compensation(symbol):
    """
    Retrieve information on how a company compensates its executives, including salary, bonus, and stock options.
    """
    url = f'https://financialmodelingprep.com/api/v4/governance/executive_compensation?symbol={symbol}&apikey={API_KEY}'
    return fetch_data(url)

def get_compensation_benchmark(year):
    """
    Compare a company's executive compensation to other companies in the same industry.
    """
    url = f'https://financialmodelingprep.com/api/v4/executive-compensation-benchmark?year={year}&apikey={API_KEY}'
    return fetch_data(url)

def get_company_notes(symbol):
    """
    Retrieve notes reported by a company in their financial statements, including information about financial condition, operations, and risks.
    """
    url = f'https://financialmodelingprep.com/api/v4/company-notes?symbol={symbol}&apikey={API_KEY}'
    return fetch_data(url)

def get_historical_employee_count(symbol):
    """
    Track how a company's workforce has grown or shrunk over time.
    """
    url = f'https://financialmodelingprep.com/api/v4/historical/employee_count?symbol={symbol}&apikey={API_KEY}'
    return fetch_data(url)

def get_employee_count(symbol):
    """
    Retrieve the current number of employees in a company.
    """
    url = f'https://financialmodelingprep.com/api/v4/employee_count?symbol={symbol}&apikey={API_KEY}'
    return fetch_data(url)

def stock_screener(market_cap_more_than=None, sector=None, industry=None, country=None, limit=100):
    """
    Find stocks that meet specific investment criteria such as market cap, sector, industry, and country.
    """
    url = f'https://financialmodelingprep.com/api/v3/stock-screener?apikey={API_KEY}'
    if market_cap_more_than:
        url += f'&marketCapMoreThan={market_cap_more_than}'
    if sector:
        url += f'&sector={sector}'
    if industry:
        url += f'&industry={industry}'
    if country:
        url += f'&country={country}'
    url += f'&limit={limit}'
    return fetch_data(url)

def get_stock_grade(symbol):
    """
    Retrieve a rating of a company given by hedge funds, investment firms, and analysts.
    """
    url = f'https://financialmodelingprep.com/api/v3/grade/{symbol}?apikey={API_KEY}'
    return fetch_data(url)

def get_executives(symbol):
    """
    Retrieve information about a company's key executives.
    """
    url = f'https://financialmodelingprep.com/api/v3/key-executives/{symbol}?apikey={API_KEY}'
    return fetch_data(url)

def get_company_core_information(symbol):
    """
    Retrieve core information about a company, such as CIK, exchange, and address.
    """
    url = f'https://financialmodelingprep.com/api/v4/company-core-information?symbol={symbol}&apikey={API_KEY}'
    return fetch_data(url)

def get_market_cap(symbol):
    """
    Retrieve the current market capitalization of a company.
    """
    url = f'https://financialmodelingprep.com/api/v3/market-capitalization/{symbol}?apikey={API_KEY}'
    return fetch_data(url)

def get_historical_market_cap(symbol, limit=100, from_date=None, to_date=None):
    """
    Retrieve historical market capitalization data for a company.
    """
    url = f'https://financialmodelingprep.com/api/v3/historical-market-capitalization/{symbol}?limit={limit}&apikey={API_KEY}'
    if from_date:
        url += f'&from={from_date}'
    if to_date:
        url += f'&to={to_date}'
    return fetch_data(url)

def get_all_countries():
    """
    Retrieve a list of all countries where stocks are traded.
    """
    url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}'
    data = fetch_data(url)
    if "error" not in data:
        countries = set()
        for stock in data:
            if 'country' in stock:
                countries.add(stock['country'])
        return list(countries)
    else:
        return data