from pydantic import BaseModel,Field
from typing import Annotated,List
from datetime import date

class Input_data(BaseModel):
    store_id:Annotated[int,Field(8091,gt=0,description='enter store id')]
    sku_id:Annotated[int,Field(216418,gt=0,description='enter sku_id')]
    n_weeks:Annotated[int,Field(12,gt=0,description='enter n_week data forcast')]



# Output model for one forecast row
class ForecastItem(BaseModel):
    store_id: int
    sku_id: int
    week: date
    forecast: float


# Output model for full API response
class ForecastResponse(BaseModel):
    forecast: List[ForecastItem]



    