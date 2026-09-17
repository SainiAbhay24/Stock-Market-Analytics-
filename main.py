import yfinance as yf
import psycopg2
import time
from datetime import datetime

# 1. Database Connection Configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Stock_Market"
DB_USER = "Your DB"
DB_PASS = "Your Pass"

# 2. 50 Stocks List (25 Indian + 25 Global)
TICKERS = [
    # Indian Stocks (.NS)
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "WIPRO.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS", "BAJFINANCE.NS",
    "TATAMOTORS.NS", "MARUTI.NS", "M&M.NS", "ITC.NS", "HINDUNILVR.NS",
    "SUNPHARMA.NS", "LT.NS", "TATASTEEL.NS", "COALINDIA.NS", "BHARTIARTL.NS",
    "ADANIENT.NS", "ADANIPORTS.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS",
    # Global Stocks
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "NVDA", "AMD", "INTC", "QCOM", "TSLA",
    "NFLX", "WMT", "ORCL", "CRM", "ADBE",
    "BABA", "NKE", "DIS", "COIN", "CSCO",
    "PYPL", "UBER", "ABNB", "SONY", "PLTR"
]

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def fetch_and_update_stocks():
    conn = get_db_connection()
    cursor = conn.cursor()

    # USD to INR Live Forex Rate Fetch
    try:
        usd_inr_ticker = yf.Ticker("INR=X")
        usd_inr_rate = usd_inr_ticker.fast_info['lastPrice']
    except Exception:
        usd_inr_rate = 83.85  # Fallback standard rate

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Live update shuru... (USD/INR Spot: {usd_inr_rate:.2f})")

    for symbol in TICKERS:
        try:
            stock = yf.Ticker(symbol)
            info = stock.fast_info
            
            # Fetch latest figures
            todays_close = round(float(info['lastPrice']), 2)
            open_price = round(float(info['open']), 2)
            prev_close = round(float(info['previousClose']), 2)
            low_price = round(float(info['dayLow']), 2)
            high_price = round(float(info['dayHigh']), 2)
            week_52_low = round(float(info['yearLow']), 2)
            week_52_high = round(float(info['yearHigh']), 2)
            
            price_change = round(todays_close - prev_close, 2)
            percent_change = round((price_change / prev_close) * 100, 2)
            trend = "GROWING" if price_change >= 0 else "DOWN"
            
            is_indian = symbol.endswith(".NS")
            rate = 1.00 if is_indian else usd_inr_rate
            price_inr = todays_close if is_indian else round(todays_close * usd_inr_rate, 2)
            
            # SQL UPDATE Query
            update_query = """
                UPDATE public.stock_market_data
                SET open_price = %s,
                    todays_close_price = %s,
                    previous_close = %s,
                    todays_low = %s,
                    todays_high = %s,
                    week_52_low = %s,
                    week_52_high = %s,
                    price_change = %s,
                    percent_change = %s,
                    trend_status = %s,
                    exchange_rate = %s,
                    current_price_inr = %s,
                    updated_at = NOW()
                WHERE ticker = %s;
            """
            cursor.execute(update_query, (
                open_price, todays_close, prev_close, low_price, high_price,
                week_52_low, week_52_high, price_change, percent_change,
                trend, rate, price_inr, symbol
            ))
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Database successfully updated!")

# --- AUTOMATION LOOP 
if __name__ == "__main__":
    while True:
        fetch_and_update_stocks()
        print("Next update in 60 seconds....(Press Ctrl+C to stop)")
        time.sleep(60)
