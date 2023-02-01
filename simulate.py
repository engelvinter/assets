import argparse
import yfinance as yf
import yaml
import pandas as pd

def get_history(symbol, period):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period)["Close"]
    df.name = symbol
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulates momentum strategy using given portfolio")
    parser.add_argument("-p", "--portfolio", dest="portfolio", type=str, required = True, help="portfolio file name")
    args = parser.parse_args()

    try:
        f = open(args.portfolio)
        list = yaml.safe_load(f)
        
        data = []
        for ticker in list:
            history = get_history(ticker, "max")
            data.append(history)

        # Using inner join to reduce index to only existing dates per asset
        df = pd.concat(data, join="inner", axis = 1)
        print(df)

    except (FileNotFoundError) as e:
        print(e)
