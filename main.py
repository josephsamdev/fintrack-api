from fastapi import FastAPI
import yfinance as yf

#Initialising the FastAPI app
app = FastAPI()

# Root endpoint - this confirms that the API is running
@app.get("/")
def root():
    return {"message": "Welcome to fintrack-api"}

# The endpoint to get the current stock price for a given ticker symbol
@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    try:

        # Fetching stock data from Yahoo Finance
        stock = yf.Ticker(ticker)
        info = stock.fast_info

        # If no price is returned, ticker is likely invalid
        if info.last_price is None:
            raise ValueError("Invalid ticker")

        # Return key price and market data, rounded for clean output
        return {
            "ticker": ticker.upper(),
            "current_price": round(info.last_price, 2),
            "market_cap": round(info.market_cap),
            "currency": info.currency
        }
    # If any error occurs, return a clean error message instead of crashing
    except Exception as e:
        return {"error": f"Could not retrieve data for ticker '{ticker.upper()}'. Please check the ticker symbol and try again."}
    

# Endpoint to retrieve history daily price data for a given ticker and time period 
@app.get("/stock/{ticker}/history")
def get_stock_history(ticker: str, period: str = "1mo"):
    try:
        # Fetch historical price data from Yahoo finance
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)

        # If the dataframe is empty, it's likely the ticker is invalid
        if history.empty:
            return {"error": f"Could not retrieve history for ticker '{ticker.upper()}'. Please check the ticker symbol and try again."}

        # Loop through each tading day, extract OHLVC data and append to list
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
