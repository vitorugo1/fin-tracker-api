from fastapi import APIRouter
from utils import df_to_json
import yfinance as yf


router = APIRouter()
dat = yf.Ticker("PETR4.SA")


@router.get('/finances')
def read_root():
    return df_to_json(dat.history(period='1mo'))