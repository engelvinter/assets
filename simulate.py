import argparse
import yfinance as yf
import yaml
import pandas as pd

from dataclasses import dataclass

@dataclass
class Asset:
    symbol: str
    price: float
    amount: float

@dataclass
class Portfolio:
    cash: float
    assets : list

def get_symbol_prices(symbol, period):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period)["Close"]
    df.name = symbol
    return df

def get_asset_prices(symbol_list):
    data = []
    for ticker in symbol_list:
        history = get_symbol_prices(ticker, "max")
        data.append(history)

    # Using inner join to reduce index to only existing dates for every asset
    df = pd.concat(data, join="inner", axis = 1)
    # Assure only business days are in the index
    df = df.asfreq('B')
    return df.dropna()

def calc_momentum_score(asset_prices):
    df3 = asset_prices.pct_change(90)
    df6 = asset_prices.pct_change(180)
    df12 = asset_prices.pct_change(360)

    mom = (df3 + df6 + df12) / 3

    return mom.dropna()

def evaluate(portfolio, asset_prices, scores):
    max_asset_index = scores.nlargest(3).index
    date = scores.name
    closes = asset_prices.loc[date]

    # sell all
    if len(portfolio.assets) > 0:
        for asset in portfolio.assets:
            portfolio.cash += asset.amount * closes[asset.symbol]
        portfolio.assets.clear()

    portfolio_value = portfolio.cash
    invest = portfolio.cash / 3

    # buy new
    for asset in max_asset_index:
        portfolio.cash -= invest

        a = Asset(asset,
                  closes[asset],
                  invest / closes[asset])
        portfolio.assets.append(a)

    return pd.Series([max_asset_index.to_list(), portfolio_value], index=["Assets", "Portfolio Value"])

def simulate(portfolio, asset_prices, momentum_score, freq):
    score = momentum_score.groupby(pd.Grouper(freq=freq)).tail(1)
    tmp = score.apply(lambda scores: evaluate(portfolio, asset_prices, scores), axis = 1)
    return tmp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulates momentum strategy using given portfolio")
    parser.add_argument("portfolio", type=str, help="portfolio file name")
    args = parser.parse_args()

    try:
        f = open(args.portfolio)
        assets = yaml.safe_load(f)

        df = get_asset_prices(assets.keys())
        mom = calc_momentum_score(df)

        p = Portfolio(10000, [])
        tmp = simulate(p, df, mom, "M")

        with open('simulate.txt', 'w') as f:
            f.write(tmp.to_csv())

    except (FileNotFoundError) as e:
        print(e)
