from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to fintrack-api"}

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.fast_info
    
    return {
        "ticker": ticker.upper(),
        "current_price": info.last_price,
        "market_cap": info.market_cap,
        "currency": info.currency
    }