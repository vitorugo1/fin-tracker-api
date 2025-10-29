import yfinance as yf
import pandas as pd

def df_to_json(df: pd.DataFrame):
    json_string = df.to_json()
    return json_string