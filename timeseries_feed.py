import time
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
import yfinance as yf

# Database Connection Details
DB_CONFIG = {
    "dbname": "Stock_Market",      
    "user": "postgres",            
    "password": "Sainiabhay24",    
    "host": "localhost",
    "port": "5432",
}


# Tickers & Company Mapping (Total 50 Stocks)
TICKERS = {
    # --- Indian Market (NSE) - 25 Companies ---
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "INFY.NS": "Infosys",
    "ICICIBANK.NS": "ICICI Bank",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "SBIN.NS": "State Bank of India",
    "BHARTIARTL.NS": "Bharti Airtel",
    "ITC.NS": "ITC Limited",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "LT.NS": "Larsen & Toubro",
    "AXISBANK.NS": "Axis Bank",
    "HCLTECH.NS": "HCL Technologies",
    "BAJFINANCE.NS": "Bajaj Finance",
    "ASIANPAINT.NS": "Asian Paints",
    "MARUTI.NS": "Maruti Suzuki",
    "SUNPHARMA.NS": "Sun Pharma",
    "TITAN.NS": "Titan Company",
    "TATAMOTORS.NS": "Tata Motors",
    "WIPRO.NS": "Wipro",
    "ADANIENT.NS": "Adani Enterprises",
    "ADANIPORTS.NS": "Adani Ports",
    "POWERGRID.NS": "Power Grid Corporation",
    "NTPC.NS": "NTPC Limited",
    "M&M.NS": "Mahindra & Mahindra",

    # --- Foreign Market (US / Global) - 25 Companies ---
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "AMZN": "Amazon.com",
    "GOOGL": "Alphabet (Google)",
    "META": "Meta Platforms",
    "TSLA": "Tesla Inc.",
    "BRK-B": "Berkshire Hathaway",
    "JNJ": "Johnson & Johnson",
    "V": "Visa Inc.",
    "JPM": "JPMorgan Chase",
    "WMT": "Walmart (Flipkart)",
    "PG": "Procter & Gamble",
    "MA": "Mastercard",
    "UNH": "UnitedHealth Group",
    "HD": "Home Depot",
    "DIS": "Walt Disney",
    "NFLX": "Netflix",
    "AMD": "Advanced Micro Devices",
    "INTC": "Intel Corporation",
    "CSCO": "Cisco Systems",
    "KO": "Coca-Cola",
    "PEP": "PepsiCo",
    "PYPL": "PayPal Holdings",
    "PLTR": "Palantir Technologies",
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_and_store_timeseries():
    conn = get_db_connection()
    cursor = conn.cursor()

    print(
        f"\n[{datetime.now().strftime('%H:%M:%S')}] Fetching intraday 5-min intervals..."
    )

    query = """
        INSERT INTO stock_timeseries_data (
            ticker, company_name, timestamp, open_price, high_price, low_price, close_price, volume
        ) VALUES %s
        ON CONFLICT (ticker, timestamp) 
        DO UPDATE SET 
            close_price = EXCLUDED.close_price,
            high_price = EXCLUDED.high_price,
            low_price = EXCLUDED.low_price,
            volume = EXCLUDED.volume;
    """

    for ticker_symbol, comp_name in TICKERS.items():
        try:
            # 5 din da 5-minute interval data
            stock = yf.Ticker(ticker_symbol)
            hist = stock.history(period="5d", interval="5m")

            if hist.empty:
                continue

            records = []
            for dt, row in hist.iterrows():
                # Timestamp nu timezone-free standard datetime format vich convert karo
                clean_timestamp = dt.to_pydatetime().replace(tzinfo=None)
                records.append(
                    (
                        ticker_symbol,
                        comp_name,
                        clean_timestamp,
                        round(float(row["Open"]), 2),
                        round(float(row["High"]), 2),
                        round(float(row["Low"]), 2),
                        round(float(row["Close"]), 2),
                        int(row["Volume"]),
                    )
                )

            if records:
                execute_values(cursor, query, records)
                conn.commit()
                print(f"✓ Saved {len(records)} candles for {comp_name}")

        except Exception as e:
            print(f"Error fetching {ticker_symbol}: {e}")
            conn.rollback()

    cursor.close()
    conn.close()
    print("Database sync complete. Sleeping for 60 seconds...")


if __name__ == "__main__":
    print("Starting Live Timeseries Polling Engine...")
    while True:
        try:
            fetch_and_store_timeseries()
        except Exception as err:
            print(f"Pipeline error: {err}")
        time.sleep(60)
        