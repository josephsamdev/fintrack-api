# fintrack-api
A REST API for querying live and historical financial market data, built with Python and FastAPI.

## Overview

fintrack-api is a backend REST API that allows users to query real-time and historical stock market data. It exposes clean endpoints for retrieving stock prices, price history, and key financial metrics such as moving averages.
Built as a portfolio project to demonstrate backend development and financial data engineering skills relevant to fintech.

## Tech stack

- Python 3.11
- FastAPI
- yfinance
- uvicorn

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/josephsamdev/fintrack-api.git
cd fintrack-api
```
### 2. Create and activate a virtual environment 
```bash
python3 -m venv venv 
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the API
```bash
uvicorn main:app --reload 
```
The API will be available at http://127.0.0.1:8000

## Endpoints 

### Get current stock price 
GET /stock/{ticker}

Example: /stock/AAPL

Response:
```json
{
    "ticker": "AAPL",
    "current_price": 339.36,
    "market_cap": 4948300000000,
    "currency": "USD"
}
```
### Get historical price data
GET /stock/{ticker}/history?period={period}

Example: /stock/AAPL/history?period=1mo

Supported periods: 1mo, 3mo, 6mo, 1y

Response:
```json
{
    "ticker": "AAPL",
    "period": "1mo",
    "data": [
        {
            "date": "2026-07-01",
            "open": 293.44,
            "close": 294.38,
            "high": 296.59,
            "low": 289.2,
            "volume": 50164200
        }
    ]
}
```
### Get Simple Moving Average (SMA) 
GET /stock/{ticker}/sma?period={period}&window={window}

Example: /stock/AAPL/sma?period=3mo&window=20

Response:
```json
{
    "ticker": "AAPL",
  "period": "3mo",
  "window": 20,
  "data": [
    {
      "date": "2026-07-01",
      "close": 294.38,
      "sma": 294.88
    }
  ]
}
```
## Error Handling

All endpoints return a clear error message for invalid tickers:
```json
{
    "error": "Could not retrieve data for ticker 'INVALID'. Please check the ticker symbol and try again."
}
```
## Author 

Joseph Sam
github.com/josephsamdev
