from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from ml_model import pipeline,last_data ,MODEL_VERSION  #model,last_data
from ml_model import forecast_sales  #ml  model
from pydantic1 import Input_data,ForecastResponse



app=FastAPI()


@app.get('/')
def hello():
    return {'message':'this is forcasting sale api'}

@app.get('/health')               
def health_check() -> dict :                #for machine visualisation
    return {
            'status':'ok',
            'version':MODEL_VERSION,    #added manually here
            'model_loaded':pipeline is not None}


@app.post("/forecast", response_model=ForecastResponse)
#pydantic model verify data type
def get_forecast(data: Input_data):
    try:

        if data.store_id not in last_data["store_id"].values:
            raise HTTPException(status_code=404, detail="Store ID not found in train data")

        if data.sku_id not in last_data["sku_id"].values:
            raise HTTPException(status_code=404, detail="SKU ID not found in train data")
    
        result = forecast_sales(
            data.store_id,
            data.sku_id,
            data.n_weeks,
            last_data,
            pipeline
        )
        # take from datetime only date 
        for r in result:
            r["week"] = r["week"].split("T")[0]
        return JSONResponse(status_code=200,content={"forecast": result})
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Forecast generation failed store_id {data.store_id} has not available sku_id {data.sku_id}: {str(e)}")