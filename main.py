from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to fintrack-api"}

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.fast_info
        
        if info.last_price is None:
            raise ValueError("Invalid ticker")
        
        return {
            "ticker": ticker.upper(),
            "current_price": round(info.last_price, 2),
            "market_cap": round(info.market_cap),
            "currency": info.currency
        }
    except Exception as e:
        return {"error": f"Could not retrieve data for ticker '{ticker.upper()}'. Please check the ticker symbol and try again."}
    

@app.get("/stock/{ticker}/history")
def get_stock_history(ticker: str, period: str = "1mo"):
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        
        if history.empty:
            return {"error": f"Could not retrieve history for ticker '{ticker.upper()}'. Please check the ticker symbol and try again."}
        
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
    except Exception as e:
        return {"error": f"Could not retrieve history for ticker '{ticker.upper()}'. Please check the ticker symbol and try again."}

@app.get("/stock/{ticker}/sma")
def get_sma(ticker: str, period: str = "3mo", window: int = 20):
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)

        if history.empty:
            return {"error": f"Could not retrieve SMA data for ticker '{ticker.upper()}'. Please check the ticker symbol and try again."}

        history["SMA"] = history["Close"].rolling(window=window).mean().round(2)

        data = []
        for date, row in history.iterrows():
            data.append({
                "date": str(date.date()),
                "close": round(row["Close"], 2),
                "sma": None if str(row["SMA"]) == "nan" else row["SMA"]
            })

        return {
        "ticker": ticker.upper(),
        "period": period,
        "window": window,
        "data": data
        }    
    except Exception as e:
        return {"error": f"Could not retrieve history for ticker '{ticker.upper()}'. Please check the ticker symbol and try again."}
