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

@app.get("/stock/{ticker}/history")
def get_stock_history(ticker: str, period: str = "1mo"):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    data = []
    for date, row in history.iterrows():
        data.append({
            "date": str(date.date()),
            "open": round(row["Open"], 2),
            "close": round(row["Close"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "volume": int(row["Volume"])

        })

    return {
        "ticker": ticker.upper(),
        "period": period,
        "data": data
    }