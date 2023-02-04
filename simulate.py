import argparse
import yfinance as yf
import yaml
import pandas as pd

def get_symbol_history(symbol, period):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period)["Close"]
    df.name = symbol
    return df

def get_portfolio_history(symbol_list):
    data = []
    for ticker in symbol_list:
        history = get_symbol_history(ticker, "max")
        data.append(history)

    # Using inner join to reduce index to only existing dates per asset
    df = pd.concat(data, join="inner", axis = 1)
    return df

def calc_momentum_score(portfolio_history):
    df1 = portfolio_history.pct_change(30).dropna()
    df3 = portfolio_history.pct_change(90).dropna()
    df6 = portfolio_history.pct_change(180).dropna()
    df12 = portfolio_history.pct_change(360).dropna()

    first_date = max(df1.index[0], df3.index[0], df6.index[0], df12.index[0])
    last_date = min(df1.index[-1], df3.index[-1], df6.index[-1], df12.index[-1])
    common_index = pd.date_range(first_date, last_date)

    cdf1 = df1.reindex(common_index)
    cdf3 = df3.reindex(common_index)
    cdf6 = df6.reindex(common_index)
    cdf12 = df12.reindex(common_index)

    mom = cdf1 + cdf3 + cdf6 + cdf12
    return mom

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulates momentum strategy using given portfolio")
    parser.add_argument("-p", "--portfolio", dest="portfolio", type=str, required = True, help="portfolio file name")
    args = parser.parse_args()

    try:
        f = open(args.portfolio)
        assets = yaml.safe_load(f)

        df = get_portfolio_history(assets.keys())
        mom = calc_momentum_score(df)
        print(mom)

    except (FileNotFoundError) as e:
        print(e)
