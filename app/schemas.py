from pydantic import BaseModel, Field
from datetime import date

# Chart model
class ChartDataPoint(BaseModel):
    date: date
    price: float = Field(..., description="Closing price for the day")

# Main asset data model
class AssetData(BaseModel):
    # ID
    ticker: str = Field(..., description="Asset ticker")
    name: str = Field(..., description="Asset name")
    currency: str = Field(..., description="Currency price (ex: BRL, USD)")
    logo_url: str | None = Field(..., description="")

    # Price data
    current_price: float
    day_change_percentage: float

    # Chart data
    six_month_chart: list[ChartDataPoint]

    class Config:
        from_attributes = True

