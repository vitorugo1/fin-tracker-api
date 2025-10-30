import yfinance as yf
import pandas as pd
from . import schemas

def _calculate_day_change(current_price: float, previous_close: float) -> float:
    if previous_close == 0:
        return 0.0
    change = ((current_price - previous_close) / previous_close) * 100
    return round(change, 2)

def _format_chart_data(history_df: pd.DataFrame) -> list[schemas.ChartDataPoint]:
    chart_data = []

    # History df has 'Date' as index
    for index_date, row in history_df.iterrows():
        chart_data.append(
            schemas.ChartDataPoint(
                date=index_date.date(), # converts timestamp to date
                price=row['Close']
            )
        )
    return chart_data

def _format_multiple_chart_data(history_series: pd.Series): 
    chart_data = []
    
    # (index, value)
    for index_date, price in history_series.items():
        
        if pd.isna(price): # checking for 'nan'
            continue
        
        chart_data.append(
            schemas.ChartDataPoint(
                date=index_date.date(),
                price=price 
            )
        )
    return chart_data

def get_asset_details(ticker_symbol: str) -> schemas.AssetData:
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # history data for the chart
        history = ticker.history(period="6mo", interval="1d")

        current_price = info.get('currentPrice', 0.0)
        previous_close = info.get('previousClose', 0.0)

        day_change = _calculate_day_change(current_price, previous_close)
        chart_points = _format_chart_data(history)

        asset_data = schemas.AssetData(
            ticker=ticker_symbol,
            name=info.get('shortName', 'Nome não encontrado'),
            currency=info.get('currency', 'N/A'),
            logo_url=info.get('logo_url', None),
            current_price=current_price,
            day_change_percentage=day_change,
            six_month_chart=chart_points
        )
        
        return asset_data

    except Exception as e:
        raise ValueError(f"Unable to fetch data for current ticker: {ticker_symbol} {e}")
    
def multiple_assets_details(ticker_list: list[str]) -> list[schemas.AssetData]:
    try:
        tickers_str = " ".join(ticker_list)
        ticker_obj = yf.Tickers(tickers_str)

        # Downloading history data to avoid too many calls
        history_data = yf.download(ticker_list, period="6mo", interval="1d")
        
        results = []

        for ticker_symbol in ticker_list:
            history = history_data['Close'][ticker_symbol]

            info = ticker_obj.tickers[ticker_symbol].info 
            current_price = info.get('currentPrice', 0.0)
            previous_close = info.get('previousClose', 0.0)
            
            day_change = _calculate_day_change(current_price, previous_close)
            chart_points = _format_multiple_chart_data(history) 


            asset_data = schemas.AssetData(
                ticker=ticker_symbol,
                name=info.get('shortName', 'Nome não encontrado'),
                currency=info.get('currency', 'N/A'),
                logo_url=info.get('logo_url', None),
                current_price=current_price,
                day_change_percentage=day_change,
                six_month_chart=chart_points
            )

            results.append(asset_data)
        
        return results

    except Exception as e:
        raise ValueError(f"Unable to fetch data for current ticker list: {ticker_list} {e}")