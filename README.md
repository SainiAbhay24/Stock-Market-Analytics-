# 📈 Real-Time Stock Market Intelligence & Quantitative Analytics

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-Data_Analysis_Expressions-orange?style=for-the-badge)

---

### 📌 Project Overview
This project is an end-to-end Financial Data Engineering and Analytics system that pipelines, stores, and visualizes real-time and intra-day market data across **50 leading Indian (NSE/BSE)** and **US (NASDAQ/NYSE)** equities. It functions as an institutional-grade trading terminal providing actionable insights into price action momentum, valuation multiples, and sector rotation.

---

### 🏗️ System Architecture

1. **Automated Timeseries Pipeline (`timeseries_feed.py` & `stock.py`)**: Python scripts automate real-time and historic market data fetching via APIs, simulating continuous ticker feeds with volume, OHLC, and timestamps.
2. **Database Warehouse (`PostgreSQL`)**: Clean relational time-series tables (`public.stock_timeseries_data`, `Dim_Sector`) maintain structured partitions with indexing for ultra-fast Power BI imports.
3. **Interactive BI Intelligence (`stock.pbix`)**: Power BI connects directly to PostgreSQL, featuring custom dark-mode UI/UX inspired by TradingView and Groww terminals.

---

### 🚀 Key Features

* 📊 **Live Multi-Market Watchlist**: Instant toggle between Indian & Foreign markets tracking top gainers, top losers, and market breadth.
* 🕯️ **Intraday Candlestick & Volume Terminal**: Line & stacked column hybrid architecture powered by transparent candle DAX, dynamic Error Bar wicks, and volume bars color-coded by candle direction.
* 🎯 **Dynamic Brand Identity**: High-res vector avatars generated via automated logo endpoints mapped to selected tickers.
* 📉 **Fundamental Valuation Matrix**: Interactive breakdown of P/E Ratio, P/B Ratio, Dividend Yield %, and Base Currency Exchange (USD/INR).
* 🎛️ **52-Week & Daily Price Gauges**: Radial performance gauges dynamically highlighting relative intraday spread against historical highs and lows.

---

### 🛠️ Tech Stack Used

* **Scripting & Automation**: Python 3, `psycopg2`, `requests`, `python-dotenv`
* **Relational Database**: PostgreSQL, Relational Star Schema
* **Business Intelligence**: Microsoft Power BI Desktop
* **Analytical Modeling**: Custom DAX (Dynamic measures, conditional color triggers, ratio indicators)
* **UI/UX Design**: Groww/TradingView Dark Terminal Theme (`#1E1E1E`), Hex Conditional Formatting

---

### ⚙️ How to Run This Project

1. **Clone this repository**:
   ```bash
   git clone [https://github.com/SainiAbhay24/stock-market-analytics-powerbi.git](https://github.com/SainiAbhay24/stock-market-analytics-powerbi.git)
   cd stock-market-analytics-powerbi
