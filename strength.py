import argparse
from dataclasses import dataclass
from numpy import double
import yfinance as yf
from pandas.tseries.offsets import DateOffset
import yaml

@dataclass
class AssetStats:
    compound_ma : float
    above_ma200 : bool
    ma50_gt_ma200 : bool

@dataclass
class AssetData:
    ticker : str
    name : str
    stats : AssetStats

def calc_average(df, period):
    new_df = df.last(period)
    av = new_df.Close.mean()
    return av

def calc_normalized_average(df, period):
    new_df = df.last(period)
    norm_av = (new_df.Close.mean() - new_df.Close[0]) / new_df.Close[0];
    return norm_av

def calc_compound_ma(df, ma_period):
    ma_sum = 0
    for period in ma_period:
        ma_sum += calc_normalized_average(df, DateOffset(months=period))
    return ma_sum / len(ma_period)

def calc_stats(df, ma_period):
    compound_ma = round(calc_compound_ma(df, ma_period), 2)
    ma200 = calc_average(df, "200B")
    above_ma200 = df[-1:].Close[0] > ma200
    ma50 = calc_average(df, "50B")
    ma50_gt_ma200 = ma50 > ma200
    return AssetStats(compound_ma, above_ma200, ma50_gt_ma200)

def create_report(ticker, name, asset_stats):
    s = "Ticker: {} ({})\n" \
        "Compound ma: {:.2f}\n" \
        "Close Above MA200: {}\n" \
        "MA50 above MA200: {}"
    return s.format(ticker,
                    name,
                    asset_stats.compound_ma,
                    asset_stats.above_ma200,
                    asset_stats.ma50_gt_ma200)

def get_ticker(ticker):
    ticker = yf.Ticker(ticker)
    df = ticker.history("1y")
    return df

def get_ma_period(ma_period_str):
    periods = { "136": [1, 3, 6], "3612" : [3, 6, 12], "13612" : [1, 3, 6, 12] }
    return periods[ma_period_str]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculates momentum strength of assets in portfolio")
    parser.add_argument("-p", "--portfolio", dest="portfolio", type=str, required = True, help="portfolio file name")
    parser.add_argument("-ma", dest="ma_period", type=str, choices=["136", "3612", "13612"], default="136", help="compound ma period")
    args = parser.parse_args()

    try:
        f = open(args.portfolio)
        list = yaml.safe_load(f)

        stats_per_ticker = {}
        for ticker in list:
            df = get_ticker(ticker)
            stats = calc_stats(df, get_ma_period(args.ma_period))
            stats_per_ticker[ticker] = AssetData(ticker, list[ticker]["name"], stats)

        a = sorted(stats_per_ticker.items(), key=lambda item: item[1].stats.compound_ma, reverse=True)
        for key, item in a:
            print(create_report(item.ticker, item.name, item.stats))
            print("---")
    except (FileNotFoundError) as e:
        print(e)
