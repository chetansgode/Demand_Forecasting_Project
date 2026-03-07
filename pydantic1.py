from pydantic import BaseModel,Field
from typing import Annotated

class Input_data(BaseModel):
    store_id:Annotated[int,Field(8091,gt=0,description='enter store id')]
    sku_id:Annotated[int,Field(216418,gt=0,description='enter sku_id')]
    n_weeks:Annotated[int,Field(12,gt=0,description='enter n_week data forcast')]



    