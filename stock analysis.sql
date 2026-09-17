SELECT * FROM stock_market_data;

CREATE TABLE stock_market_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    company_name VARCHAR(100),
    market_type VARCHAR(20),
    currency VARCHAR(10),
    trade_date DATE NOT NULL,

    -- Price & Start/End
    open_price NUMERIC(10, 2),            -- Start price
    todays_close_price NUMERIC(10, 2),    -- End price
    previous_close NUMERIC(10, 2),        -- Previous session close
    current_price_formatted VARCHAR(30),

    -- Growth / Down Tracking (Groww Style)
    price_change NUMERIC(10, 2),          -- Point Change (+/-)
    percent_change NUMERIC(6, 2),         -- % Gain / Loss (+/-)
    trend_status VARCHAR(10),             -- 'GROWING' ya 'DOWN'

    -- Performance Range
    todays_low NUMERIC(10, 2),
    todays_high NUMERIC(10, 2),
    week_52_low NUMERIC(10, 2),           -- 52 Week Low
    week_52_high NUMERIC(10, 2),          -- 52 Week High
    live_volume BIGINT,

    -- Groww Fundamentals
    market_cap VARCHAR(30),
    pe_ratio NUMERIC(10, 2),
    pb_ratio NUMERIC(10, 2),
    roe_percent NUMERIC(6, 2),
    eps NUMERIC(10, 2),
    dividend_yield NUMERIC(6, 2),
    debt_to_equity NUMERIC(10, 2),

    -- Forex & INR Normalization
    exchange_rate NUMERIC(10, 4) DEFAULT 1.0000,
    current_price_inr NUMERIC(12, 2),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_ticker_date UNIQUE (ticker, trade_date)
);

SELECT 
    company_name,
    market_type,
    currency,
    open_price AS start_price,
    todays_close_price AS end_price,
    previous_close,
    price_change,
    percent_change || '%' AS change_percent,
    trend_status,
    current_price_inr,
    COALESCE(pe_ratio, 0.00) AS pe_ratio,
    market_cap
FROM stock_market_data
ORDER BY market_type, company_name;

SELECT COUNT(*) FROM stock_market_data;



-- Historical te live timestamp data layi table
CREATE TABLE IF NOT EXISTS stock_timeseries_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20),
    company_name VARCHAR(100),
    timestamp TIMESTAMP WITHOUT TIME ZONE,
    open_price NUMERIC(10, 2),
    high_price NUMERIC(10, 2),
    low_price NUMERIC(10, 2),
    close_price NUMERIC(10, 2),
    volume BIGINT,
    UNIQUE(ticker, timestamp)
);

-- Query speed fast karan layi indexes
CREATE INDEX IF NOT EXISTS idx_stock_timeseries_ticker ON stock_timeseries_data(ticker);
CREATE INDEX IF NOT EXISTS idx_stock_timeseries_timestamp ON stock_timeseries_data(timestamp);