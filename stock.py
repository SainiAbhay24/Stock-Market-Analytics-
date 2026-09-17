import time
from datetime import datetime
import yfinance as yf
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "dbname": "Stock_Market",
    "user": "Your DB",
    "password": "Your Pass",
    "host": "localhost",
    "port": "5432"
}

# Exactly 50 Top Companies (25 Indian + 25 Foreign)
PORTFOLIO = [
    # --- 25 Indian Market Leaders (NSE) ---
    {"ticker": "RELIANCE.NS", "name": "Reliance Industries", "market": "Indian Market", "currency": "INR"},
    {"ticker": "COALINDIA.NS", "name": "Coal India", "market": "Indian Market", "currency": "INR"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy Services", "market": "Indian Market", "currency": "INR"},
    {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "market": "Indian Market", "currency": "INR"},
    {"ticker": "INFY.NS", "name": "Infosys", "market": "Indian Market", "currency": "INR"},
    {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "market": "Indian Market", "currency": "INR"},
    {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "market": "Indian Market", "currency": "INR"},
    {"ticker": "SBIN.NS", "name": "State Bank of India", "market": "Indian Market", "currency": "INR"},
    {"ticker": "BHARTIARTL.NS", "name": "Bharti Airtel", "market": "Indian Market", "currency": "INR"},
    {"ticker": "ITC.NS", "name": "ITC Limited", "market": "Indian Market", "currency": "INR"},
    {"ticker": "HINDUNILVR.NS", "name": "Hindustan Unilever", "market": "Indian Market", "currency": "INR"},
    {"ticker": "LT.NS", "name": "Larsen & Toubro", "market": "Indian Market", "currency": "INR"},
    {"ticker": "BAJFINANCE.NS", "name": "Bajaj Finance", "market": "Indian Market", "currency": "INR"},
    {"ticker": "MARUTI.NS", "name": "Maruti Suzuki", "market": "Indian Market", "currency": "INR"},
    {"ticker": "SUNPHARMA.NS", "name": "Sun Pharma", "market": "Indian Market", "currency": "INR"},
    {"ticker": "ADANIENT.NS", "name": "Adani Enterprises", "market": "Indian Market", "currency": "INR"},
    {"ticker": "ADANIPORTS.NS", "name": "Adani Ports", "market": "Indian Market", "currency": "INR"},
    {"ticker": "TATASTEEL.NS", "name": "Tata Steel", "market": "Indian Market", "currency": "INR"},
    {"ticker": "WIPRO.NS", "name": "Wipro", "market": "Indian Market", "currency": "INR"},
    {"ticker": "KOTAKBANK.NS", "name": "Kotak Mahindra Bank", "market": "Indian Market", "currency": "INR"},
    {"ticker": "AXISBANK.NS", "name": "Axis Bank", "market": "Indian Market", "currency": "INR"},
    {"ticker": "NTPC.NS", "name": "NTPC Limited", "market": "Indian Market", "currency": "INR"},
    {"ticker": "ONGC.NS", "name": "ONGC", "market": "Indian Market", "currency": "INR"},
    {"ticker": "POWERGRID.NS", "name": "Power Grid Corp", "market": "Indian Market", "currency": "INR"},
    {"ticker": "TITAN.NS", "name": "Titan Company", "market": "Indian Market", "currency": "INR"},
    {"ticker": "M&M.NS", "name": "Mahindra & Mahindra", "market": "Indian Market", "currency": "INR"},

    # --- 25 Foreign Market Leaders (NASDAQ / NYSE) ---
    {"ticker": "AAPL", "name": "Apple Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "GOOGL", "name": "Alphabet (Google)", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "AMZN", "name": "Amazon.com", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "NVDA", "name": "NVIDIA", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "TSLA", "name": "Tesla Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "META", "name": "Meta Platforms", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "WMT", "name": "Walmart (Flipkart)", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "NFLX", "name": "Netflix Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "INTC", "name": "Intel Corporation", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "ORCL", "name": "Oracle Corporation", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "CRM", "name": "Salesforce Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "ADBE", "name": "Adobe Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "BABA", "name": "Alibaba Group", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "NKE", "name": "Nike Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "DIS", "name": "Walt Disney Company", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "COIN", "name": "Coinbase Global", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "QCOM", "name": "Qualcomm Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "CSCO", "name": "Cisco Systems", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "PYPL", "name": "PayPal Holdings", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "UBER", "name": "Uber Technologies", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "ABNB", "name": "Airbnb Inc.", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "SONY", "name": "Sony Group Corp", "market": "Foreign Market", "currency": "USD"},
    {"ticker": "PLTR", "name": "Palantir Technologies", "market": "Foreign Market", "currency": "USD"}
]

def format_market_cap(val, currency):
    if not val:
        return "N/A"
    if currency == "INR":
        crores = val / 10000000
        return f"₹{crores:,.0f}Cr"
    billions = val / 1000000000
    return f"${billions:,.2f}B"

def get_live_usd_inr_rate():
    try:
        forex = yf.Ticker("USDINR=X").history(period="1d")
        if not forex.empty:
            return round(float(forex['Close'].iloc[-1]), 4)
    except Exception:
        pass
    return 86.50

def run_pipeline():
    upsert_query = """
        INSERT INTO stock_market_data (
            ticker, company_name, market_type, currency, trade_date,
            open_price, todays_close_price, previous_close, current_price_formatted,
            price_change, percent_change, trend_status,
            todays_low, todays_high, week_52_low, week_52_high, live_volume,
            market_cap, pe_ratio, pb_ratio, roe_percent, eps, dividend_yield, debt_to_equity,
            exchange_rate, current_price_inr, updated_at
        ) VALUES %s
        ON CONFLICT (ticker, trade_date) DO UPDATE SET
            open_price = EXCLUDED.open_price,
            todays_close_price = EXCLUDED.todays_close_price,
            previous_close = EXCLUDED.previous_close,
            current_price_formatted = EXCLUDED.current_price_formatted,
            price_change = EXCLUDED.price_change,
            percent_change = EXCLUDED.percent_change,
            trend_status = EXCLUDED.trend_status,
            todays_low = EXCLUDED.todays_low,
            todays_high = EXCLUDED.todays_high,
            week_52_low = EXCLUDED.week_52_low,
            week_52_high = EXCLUDED.week_52_high,
            live_volume = EXCLUDED.live_volume,
            market_cap = EXCLUDED.market_cap,
            pe_ratio = EXCLUDED.pe_ratio,
            pb_ratio = EXCLUDED.pb_ratio,
            roe_percent = EXCLUDED.roe_percent,
            eps = EXCLUDED.eps,
            dividend_yield = EXCLUDED.dividend_yield,
            debt_to_equity = EXCLUDED.debt_to_equity,
            exchange_rate = EXCLUDED.exchange_rate,
            current_price_inr = EXCLUDED.current_price_inr,
            updated_at = CURRENT_TIMESTAMP;
    """

    while True:
        cycle_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n=======================================================")
        print(f"Sync Cycle Started: {cycle_time}")

        usd_to_inr = get_live_usd_inr_rate()
        print(f"Live USD/INR Rate: ₹{usd_to_inr}")

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            batch_records = []

            for item in PORTFOLIO:
                ticker = item["ticker"]
                name = item["name"]
                market = item["market"]
                curr = item["currency"]

                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="5d")
                    if hist.empty:
                        continue

                    hist.reset_index(inplace=True)
                    today_row = hist.iloc[-1]
                    trade_date = pd.to_datetime(today_row['Date']).date()

                    open_val = round(float(today_row['Open']), 2)
                    close_val = round(float(today_row['Close']), 2)
                    high_val = round(float(today_row['High']), 2)
                    low_val = round(float(today_row['Low']), 2)
                    vol = int(today_row['Volume'])

                    if len(hist) >= 2:
                        prev_close = round(float(hist.iloc[-2]['Close']), 2)
                        p_change = round(close_val - prev_close, 2)
                        pct_change = round(((close_val - prev_close) / prev_close) * 100, 2)
                    else:
                        prev_close = open_val
                        p_change = 0.00
                        pct_change = 0.00

                    trend = "GROWING" if p_change >= 0 else "DOWN"

                    if curr == "USD":
                        price_formatted = f"${close_val:,.2f}"
                        rate_used = usd_to_inr
                        price_inr = round(close_val * rate_used, 2)
                    else:
                        price_formatted = f"₹{close_val:,.2f}"
                        rate_used = 1.0000
                        price_inr = close_val

                    # Fundamentals
                    info = stock.info or {}
                    w52_low = round(float(info.get('fiftyTwoWeekLow', 0)), 2)
                    w52_high = round(float(info.get('fiftyTwoWeekHigh', 0)), 2)
                    m_cap = format_market_cap(info.get('marketCap'), curr)
                    pe = round(float(info.get('trailingPE', 0)), 2) if info.get('trailingPE') else None
                    pb = round(float(info.get('priceToBook', 0)), 2) if info.get('priceToBook') else None
                    roe = round(float(info.get('returnOnEquity', 0)) * 100, 2) if info.get('returnOnEquity') else None
                    eps = round(float(info.get('trailingEps', 0)), 2) if info.get('trailingEps') else None
                    div_yield = round(float(info.get('dividendYield', 0)) * 100, 2) if info.get('dividendYield') else None
                    debt_eq = round(float(info.get('debtToEquity', 0)) / 100, 2) if info.get('debtToEquity') else None

                    batch_records.append((
                        ticker, name, market, curr, trade_date,
                        open_val, close_val, prev_close, price_formatted,
                        p_change, pct_change, trend,
                        low_val, high_val, w52_low, w52_high, vol,
                        m_cap, pe, pb, roe, eps, div_yield, debt_eq,
                        rate_used, price_inr, datetime.now()
                    ))

                except Exception as inner_err:
                    print(f"Skipping {ticker}: {inner_err}")

            if batch_records:
                execute_values(cursor, upsert_query, batch_records)
                conn.commit()
                print(f"✅ Synced {len(batch_records)} companies into PostgreSQL.")

            cursor.close()
            conn.close()

        except Exception as db_err:
            print(f"❌ Database error: {db_err}")

        print("Cycle done. Next refresh in 10s...")
        time.sleep(10)

if __name__ == "__main__":
    run_pipeline()
