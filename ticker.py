import argparse
import yfinance as yf

def get_history(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="max")
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Displays information about stock ticker")
    parser.add_argument("symbol", type=str, help="symbol of the ticker")
    args = parser.parse_args()

    df = get_history(args.symbol)
    print("Symbol: {}".format(args.symbol))
    print("Start: {}".format(df.head(1).index[0]))
    pct_change = df.Close.resample('A').last().pct_change().dropna() * 100
    print(pct_change.to_string(float_format=lambda x: "{:.1f} %".format(x)))
