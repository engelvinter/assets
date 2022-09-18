import argparse
from dataclasses import dataclass
from numpy import double
import yfinance as yf
from pandas.tseries.offsets import DateOffset

@dataclass
class AssetStats:
    relative_ma : float
    above_ma200 : bool
    ma50_gt_ma200 : bool

@dataclass
class AssetData:
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

def calc_relative_ma(df):
    ma_sum = calc_normalized_average(df, DateOffset(months=12))
    ma_sum += calc_normalized_average(df, DateOffset(months=6))
    ma_sum += calc_normalized_average(df, DateOffset(months=3))
    ma_sum += calc_normalized_average(df, DateOffset(months=1))
    return ma_sum / 3

def calc_stats(df):
    relative_ma = round(calc_relative_ma(df), 2)
    ma200 = calc_average(df, "200B")
    above_ma200 = df[-1:].Close[0] > ma200
    ma50 = calc_average(df, "50B")
    ma50_gt_ma200 = ma50 > ma200
    return AssetStats(relative_ma, above_ma200, ma50_gt_ma200)

def create_report(ticker, asset_stats):
    s = "Ticker: {}\n" \
        "Relative ma: {:.2f}\n" \
        "Close Above MA200: {}\n" \
        "MA50 above MA200: {}"
    return s.format(ticker,
                    asset_stats.relative_ma,
                    asset_stats.above_ma200,
                    asset_stats.ma50_gt_ma200)

def get_stats(ticker):
    ticker = yf.Ticker(ticker)
    df = ticker.history("1y")
    stats = calc_stats(df)
    return stats

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('ticker', type=str, help='ticker symbol')
    #args = parser.parse_args()

    l = [ ("IVV", "Core S&P 500"), 
          ("EUNK.F", "MSCI Europe"),
          ("XDJP.F", "Nikkei 225"),
          ("XMME.F", "MSCI Emerging Markets"),
          ("SXR1.F", "MSCI Pacific ex. Japan"), 
          ("IQQP.F", "European Property Yield"), 
          ("M9SA.F", "Rogers Int. Commodity Index"),
          ("GC=F", "Gold"),
          ("JPGL.F", "Global Equity multi factor"),
          ("UIMB.F", "TIPS 10+ years")]

    stats_per_ticker = {}
    for ticker in l:
        stats = get_stats(ticker[0])
        stats_per_ticker[ticker] = AssetData(ticker[1], stats)

    a = sorted(stats_per_ticker.items(), key=lambda item: item[1].stats.relative_ma, reverse=True)
    for key, item in a:
        print(create_report(key, item.stats))

