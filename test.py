import yfinance as yf

ticker = yf.Ticker("AAPL")
info = ticker.fast_info

print(f"Stock: AAPL")
print(f"Current Price: ${info.last_price:.2f}")
print(f"Market Cap: ${info.market_cap:,.0f}")