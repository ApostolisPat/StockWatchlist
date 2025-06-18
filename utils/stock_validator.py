import yfinance as yf

def is_valid_stock_symbol(symbol: str) -> bool:
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.info.get("regularMarketPrice")
        return price is not None
    except Exception:
        return False