from fastapi import APIRouter
from .services import get_asset_details
from .services import multiple_assets_details


router = APIRouter()
dat = ["PETR4.SA", "AAPL", "GOOG"]


@router.get('/finances')
async def read_root():
    return multiple_assets_details(dat)