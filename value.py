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

df = pd.read_csv(sys.argv[1])

df_clean = clean_data(df.copy())
df_clean.head()
print(df)