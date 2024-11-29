#!/usr/bin/env python
# coding: utf-8

# # PROCESS

# Agentic system to retrieve financial data about a company:
# 
# 1. Using LlamaIndex
# 
# 2. Using Anthropic : Claude 3.5 sonnet
# 
# 3. Using Financial Modeling Prep API, in which you can
# provide several information:
# 
#   * Stock Prices, EPS, PE,...
# 
#   * Company basic information: Sector, Industry, Market Cap, description, beta,...
# 
#   * Income statement
# 
#   You can also fetch from Financial Modeling Prep API:
# 
#   * Balance Sheet
# 
#   * Cash Flow
# 
#   * Key Metrics
# 
# 
# 

# In[2]:


# !pip install llama-index-llms-anthropic -q
# !pip install llama-index -q

# In[8]:

import os
from llama_index.llms.anthropic import Anthropic
from llama_index.core.tools import FunctionTool

import nest_asyncio

from utils.data_utils import load_functions_from_directory

nest_asyncio.apply()

#   Other endpoints are not free:
# 
#   * News
# 
#   * News Sentiment
# 
#   * ...
#   

# # Anthropic LLM and API keys

# In[9]:

CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
FINANCIAL_MODELING_PREP_API_KEY = os.environ.get('FINANCIAL_MODELING_PREP_API_KEY')
print("Claude API Key = ",CLAUDE_API_KEY)
print("Financial Modeling API Key = ", FINANCIAL_MODELING_PREP_API_KEY)

# “Data provided by Financial Modeling Prep”
# 
# https://financialmodelingprep.com/developer/docs/.

# In[10]:


llm_anthropic = Anthropic(model="claude-3-5-sonnet-20240620", api_key=CLAUDE_API_KEY)

# # Tools

# In[25]:


# get_stock_price, get_company_financials, get_income_statement

# ## get_stock_price

# In[22]:


import requests


# Define the functions that will fetch financial data
def get_stock_price(symbol):
    """
    Fetch the current stock price for the given symbol, the current volume, the average price 50d and 200d, EPS, PE and the next earnings Announcement.
    """
    url = f"https://financialmodelingprep.com/api/v3/quote-order/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        price = data[0]['price']
        volume = data[0]['volume']
        priceAvg50 = data[0]['priceAvg50']
        priceAvg200 = data[0]['priceAvg200']
        eps = data[0]['eps']
        pe = data[0]['pe']
        earningsAnnouncement = data[0]['earningsAnnouncement']
        return {"symbol": symbol.upper(), "price": price, "volume": volume, "priceAvg50": priceAvg50,
                "priceAvg200": priceAvg200, "EPS": eps, "PE": pe, "earningsAnnouncement": earningsAnnouncement}
    except (IndexError, KeyError):
        return {"error": f"Could not fetch price for symbol: {symbol}"}


## DATA PROVIDED BY THIS ENDPOINT:
# [{'symbol': 'AAPL',
#   'name': 'Apple Inc.',
#   'price': 222.5,
#   'changesPercentage': -0.1212,
#   'change': -0.27,
#   'dayLow': 221.91,
#   'dayHigh': 224.03,
#   'yearHigh': 237.23,
#   'yearLow': 164.08,
#   'marketCap': 3382912250000,
#   'priceAvg50': 223.0692,
#   'priceAvg200': 195.382,
#   'exchange': 'NASDAQ',
#   'volume': 35396922,
#   'avgVolume': 57548506,
#   'open': 223.58,
#   'previousClose': 222.77,
#   'eps': 6.57,
#   'pe': 33.87,
#   'earningsAnnouncement': '2024-10-31T00:00:00.000+0000',
#   'sharesOutstanding': 15204100000,
#   'timestamp': 1726257601}]


# ## get_company_financials

# In[23]:


def get_company_financials(symbol):
    """
    Fetch basic financial information for the given company symbol such as the industry, the sector, the name of the company, and the market capitalization.
    """
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        results = data[0]
        financials = {
            "symbol": results["symbol"],
            "companyName": results["companyName"],
            "marketCap": results["mktCap"],
            "industry": results["industry"],
            "sector": results["sector"],
            "website": results["website"],
            "beta": results["beta"],
            "price": results["price"],
        }
        return financials
    except (IndexError, KeyError):
        return {"error": f"Could not fetch financials for symbol: {symbol}"}


## DATA PROVIDED BY THIS ENDPOINT:
# [{'symbol': 'AAPL',
#   'price': 222.5,
#   'beta': 1.24,
#   'volAvg': 57548506,
#   'mktCap': 3382912250000,
#   'lastDiv': 1,
#   'range': '164.08-237.23',
#   'changes': -0.27,
#   'companyName': 'Apple Inc.',
#   'currency': 'USD',
#   'cik': '0000320193',
#   'isin': 'US0378331005',
#   'cusip': '037833100',
#   'exchange': 'NASDAQ Global Select',
#   'exchangeShortName': 'NASDAQ',
#   'industry': 'Consumer Electronics',
#   'website': 'https://www.apple.com',
#   'description': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. In addition, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was incorporated in 1977 and is headquartered in Cupertino, California.',
#   'ceo': 'Mr. Timothy D. Cook',
#   'sector': 'Technology',
#   'country': 'US',
#   'fullTimeEmployees': '161000',
#   'phone': '408 996 1010',
#   'address': 'One Apple Park Way',
#   'city': 'Cupertino',
#   'state': 'CA',
#   'zip': '95014',
#   'dcfDiff': 55.70546,
#   'dcf': 166.79453554058594,
#   'image': 'https://financialmodelingprep.com/image-stock/AAPL.png',
#   'ipoDate': '1980-12-12',
#   'defaultImage': False,
#   'isEtf': False,
#   'isActivelyTrading': True,
#   'isAdr': False,
#   'isFund': False}]

# ## get_income_statement

# In[24]:


def get_income_statement(symbol):
    """
    Fetch last income statement for the given company symbol such as revenue,
    gross profit, net income, EBITDA, EPS.
    """
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    data = response.json()

    try:
        results = data[0]
        financials = {
            "date": results["date"],
            "revenue": results["revenue"],
            "gross profit": results["grossProfit"],
            "net income": results["netIncome"],
            "ebitda": results["ebitda"],
            "EPS": results["eps"],
            "EPS diluted": results["epsDiluted"]
        }
    except (IndexError, KeyError):
        return data, financials

    return {"error": f"Could not fetch financials for symbol: {symbol}"}


# DATA PROVIDED BY THIS ENDPOINT:
# 'date': '2023-09-30',
# 'symbol': 'AAPL',
# 'reportedCurrency': 'USD',
# 'cik': '0000320193'
#  fillingDate': '2023-11-03',
#  acceptedDate': '2023-11-02 18:08:27',
#  period': 'FY',
#  calendarYear': '2023',
#  revenue': 383285000000,
#  costOfRevenue': 214137000000,
#  grossProfit': 169148000000,
#  grossProfitRatio': 0.4413112958,
#  researchAndDevelopmentExpenses': 29915000000,
#  generalAndAdministrativeExpenses': 0,
#  sellingAndMarketingExpenses': 0,
#  sellingGeneralAndAdministrativeExpenses': 24932000000,
#  otherExpenses': 382000000,
#  operatingExpenses': 55229000000,
#  costAndExpenses': 269366000000,
#  interestIncome': 3750000000,
#  interestExpense': 3933000000,
#  depreciationAndAmortization': 11519000000,
#  ebitda': 125820000000,
#  ebitdaRatio': 0.3282674772,
#  operatingIncome': 114301000000,
#  operatingIncomeRatio': 0.2982141227,
#  totalOtherIncomeExpensesNet': -565000000,
#  incomeBeforeTax': 113736000000,
#  incomeBeforeTaxRatio': 0.2967400237,
#  incomeTaxExpense': 16741000000,
#  netIncome': 96995000000,
#  netIncomeRatio': 0.2530623426,
#  eps': 6.16,
#  epsDiluted': 6.13,
#  weightedAverageShsOut': 15744231000,
#  weightedAverageShsOutDil': 15812547000,
#  link': 'https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/0000320193-23-000106-index.htm',
#  finalLink': 'https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm'

# ## Tools

# # Anthropic Agent

# ## Convert the functions to tools function

# In[26]:


tool_stock_price = FunctionTool.from_defaults(fn=get_stock_price)
tool_company_financials = FunctionTool.from_defaults(fn=get_company_financials)
tool_income_statement = FunctionTool.from_defaults(fn=get_income_statement)

dynamic_tools = load_functions_from_directory("functions")
static_tools = [tool_income_statement, tool_company_financials, tool_stock_price]
all_tools = dynamic_tools + static_tools
# ## Create Anthropic Agent by incorporating the predefined tools:

# In[42]:


from llama_index.core.agent import FunctionCallingAgent

agent = FunctionCallingAgent.from_tools(
    all_tools,
    llm=llm_anthropic,
    verbose=False,
    allow_parallel_tool_calls=False,
)

# ## Start Chatting

# In[43]:


# query= "Give me the current price of Snowflake"
# response = agent.chat(query)
# print(str(response))

# In[34]:

# query= "What was the last revenue reported by Snowflake?"
# response = agent.chat(query)
# print(str(response))

# # ChatBot using Anthropic Agent:

# In[44]:


while True:
    user_input = input("\nQuery [type exit or quit to exit the chat]:=> ")
    if user_input.lower() in ["exit", "quit"]:
        print("Assistant: Thanks for using the chatbot!")
        break
    if user_input.lower() != "" :
        response = agent.chat(user_input)
        print(str(response))
