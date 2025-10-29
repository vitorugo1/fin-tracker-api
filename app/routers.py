from fastapi import APIRouter
from .services import get_asset_details


router = APIRouter()
dat = "PETR4.SA"


@router.get('/finances')
async def read_root():
    return get_asset_details("PETR4.SA")