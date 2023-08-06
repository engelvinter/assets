import sys
import argparse
import pandas as pd

def clean_data(df):
    # Replace missing values with "0,0" in column: 'Direktav. - Senaste'
    df = df.fillna({'Direktav. - Senaste': "0,0"})
    # Drop rows with missing data in column: 'P/S - Senaste'
    df = df.dropna(subset=['P/S - Senaste'])
    # Drop rows with missing data in column: 'P/B - Senaste'
    df = df.dropna(subset=['P/B - Senaste'])
    # Drop rows with missing data in column: 'Kursutveck. - Utveck.  1år'
    df = df.dropna(subset=['Kursutveck. - Utveck.  1år'])
    # Convert to float: Kursutveck. - Utveck.  6m
    
    Column = 'Kursutveck. - Utveck.  6m'
    
    # Step 1: Remove the percentage symbol and convert to float
    df[Column] = df[Column].str.replace(',', '.').str.rstrip('%').astype(float)
    
    # Step 2: Divide by 100 to get the decimal representation of the percentages
    df[Column] = df[Column] / 100
    
    
    # Convert to float: Kursutveck. - Utveck.  3m
    
    Column = 'Kursutveck. - Utveck.  3m'
    
    # Step 1: Remove the percentage symbol and convert to float
    df[Column] = df[Column].str.replace(',', '.').str.rstrip('%').astype(float)
    
    # Step 2: Divide by 100 to get the decimal representation of the percentages
    df[Column] = df[Column] / 100
    # Convert to float: Kursutveck. - Utveck.  1år
    
    Column = 'Kursutveck. - Utveck.  1år'
    # Step 1: Remove the percentage symbol and convert to float
    df[Column] = df[Column].str.replace(',', '.').str.rstrip('%').astype(float)
    
    # Step 2: Divide by 100 to get the decimal representation of the percentages
    df[Column] = df[Column] / 100
    # Convert to float: Direktav. - Senaste
    
    Column = 'Direktav. - Senaste'
    
    # Step 1: Remove the percentage symbol and convert to float
    df[Column] = df[Column].str.replace(',', '.').str.rstrip('%').astype(float)
    
    # Step 2: Divide by 100 to get the decimal representation of the percentages
    df[Column] = df[Column] / 100
    # Convert to float: P/E Senaste
    
    Column = 'P/E - Senaste'
    
    # Step 1: Remove the percentage symbol and convert to float
    df[Column] = df[Column].str.replace(',', '.').str.rstrip('%').astype(float)
    
    # Step 2: Divide by 100 to get the decimal representation of the percentages
    df[Column] = df[Column]
    # Convert to float: P/S Senaste
    
    Column = 'P/S - Senaste'
    
    # Step 1: Remove the percentage symbol and convert to float
    df[Column] = df[Column].str.replace(',', '.').str.rstrip('%').astype(float)
    
    # Step 2: Divide by 100 to get the decimal representation of the percentages
    df[Column] = df[Column]
    # Convert to float: P/B Senaste
    
    Column = 'P/B - Senaste'
    
    # Step 1: Remove the percentage symbol and convert to float
    df[Column] = df[Column].str.replace(',', '.').str.rstrip('%').astype(float)
    
    # Step 2: Divide by 100 to get the decimal representation of the percentages
    df[Column] = df[Column]
    return df

"""
Index(['Börsdata ID', 'Bolagsnamn', 'Kursutveck. - Utveck.  6m',
       'Kursutveck. - Utveck.  1år', 'Kursutveck. - Utveck.  3m',
       'EV/EBITDA - Senaste', 'P/FCF - Senaste', 'Utdelning - Senaste',
       'Info - Ticker', 'Direktav. - Senaste', 'P/E - Senaste',
       'P/S - Senaste', 'P/B - Senaste', 'Info - Tid', 'Info - Aktiekurs',
       'Info - Rapport', 'Info - Sektor'],
      dtype='object')
"""
def create_ranking(df):
    rankings = { 'P/E - Senaste': -1, 'P/FCF - Senaste': -1, 'P/S - Senaste': -1, 'Direktav. - Senaste': 1 }
    ratio_scores = pd.DataFrame()
    for column, rank in rankings.items():
        ratio_scores[column] = df[column].rank(ascending=rank)
    return ratio_scores

def calc_momentum(df):
    mom = df[['Kursutveck. - Utveck.  3m', 'Kursutveck. - Utveck.  6m', 'Kursutveck. - Utveck.  1år']].mean(axis=1)
    return mom

def calc_composite_value(df):
    comp_value = df.mean(axis=1)
    return comp_value

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])

    df_clean = clean_data(df.copy())
    df_clean.head()

    ranking = create_ranking(df_clean)
    df_clean['comp_value'] = calc_composite_value(ranking)
    df_clean['momentum'] = calc_momentum(df_clean)

    a = df_clean.sort_values('comp_value', ascending=True)

    print(a.head(10))
    print(a.tail(10))