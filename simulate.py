import argparse
import yfinance as yf
import yaml
import pandas as pd
import os
from dataclasses import dataclass

@dataclass
class Holding:
    symbol: str
    price: float
    amount: float

@dataclass
class Asset:
    symbol: str
    percent: int

@dataclass
class Strategy:
    name: str
    frequency: str
    assets : list

@dataclass
class Portfolio:
    cash: float
    holdings : list

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

def trend_3612(portfolio, asset_prices, scores):
    max_asset_index = scores.nlargest(3).index
    date = scores.name
    closes = asset_prices.loc[date]

    # sell all
    if len(portfolio.holdings) > 0:
        for asset in portfolio.holdings:
            portfolio.cash += asset.amount * closes[asset.symbol]
        portfolio.holdings.clear()

    portfolio_value = portfolio.cash
    invest = portfolio.cash / 3

    # buy new
    for asset in max_asset_index:
        portfolio.cash -= invest

        a = Holding(asset,
                  closes[asset],
                  invest / closes[asset])
        portfolio.holdings.append(a)

    return pd.Series([max_asset_index.to_list(), portfolio_value], index=["Assets", "Portfolio Value"])

def simulate(portfolio, asset_prices, momentum_score, strategy, freq):
    score = momentum_score.groupby(pd.Grouper(freq=freq)).tail(1)
    tmp = score.apply(lambda scores: strategy(portfolio, asset_prices, scores), axis = 1)
    return tmp

#read_strategy_configuration
#construct_strategy

def read_strategy(filename):
    f = open(filename)
    loaded_strategy = yaml.safe_load(f)
    name = loaded_strategy["strategy"]
    freq = loaded_strategy["frequency"]
    assets = []
    for symbol, values in loaded_strategy["assets"].items():
        if "percent" in values:
            percent = values["percent"]
        else:
            percent = None
        assets.append(Asset(symbol, percent))

    return Strategy(name, freq, assets)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulates momentum strategy using given portfolio")
    parser.add_argument("configurations", nargs="+", help="filename(s) to yaml configurations of strategies")
    args = parser.parse_args()

    try:
        default_strategies = { }
        default_strategies["trend_3612"] = trend_3612

        for config in args.configurations:
            strat = read_strategy(config)

            symbols = [asset.symbol for asset in strat.assets]
            prices = get_asset_prices(symbols)
            mom = calc_momentum_score(prices)

            p = Portfolio(10000, [])
            tmp = simulate(p, prices, mom, default_strategies[strat.name], strat.frequency)
        
            name = os.path.splitext(config)[0]
            with open(f'simulate_{name}.txt', 'w') as f:
                f.write(tmp.to_csv())

    except (FileNotFoundError) as e:
        print(e)
