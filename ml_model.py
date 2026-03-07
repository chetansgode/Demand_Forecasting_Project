import pandas as pd

def forecast_sales(store_id, sku_id, n_weeks, last_data, model):

    forecast_df = last_data[
        (last_data["store_id"] == store_id) &
        (last_data["sku_id"] == sku_id)
    ].copy()

    forecasts = []

    for i in range(n_weeks):

        # move week forward
        forecast_df["week"] = pd.to_datetime(forecast_df["week"]) + pd.Timedelta(weeks=1)

        # update date features
        forecast_df["weekofyear"] = forecast_df["week"].dt.isocalendar().week.astype(int)
        forecast_df["month"] = forecast_df["week"].dt.month
        forecast_df["quarter"] = forecast_df["week"].dt.quarter
        forecast_df["year"] = forecast_df["week"].dt.year

        # model input
        X_next = forecast_df.drop(
            columns=["week","units_sold","predicted_units_sold"],
            errors="ignore"
        )

        # predict
        forecast_df["predicted_units_sold"] = model.predict(X_next)

        forecast_df["predicted_units_sold"] = forecast_df["predicted_units_sold"].clip(lower=0)

        forecasts.append({
            "store_id": int(store_id),
            "sku_id": int(sku_id),
            "week": str(forecast_df["week"].values[0]),
            "forecast": float(forecast_df["predicted_units_sold"].values[0])
        })

        # update lag features
        forecast_df["lag_12"] = forecast_df["lag_8"]
        forecast_df["lag_8"] = forecast_df["lag_4"]
        forecast_df["lag_4"] = forecast_df["lag_3"]
        forecast_df["lag_3"] = forecast_df["lag_2"]
        forecast_df["lag_2"] = forecast_df["lag_1"]
        forecast_df["lag_1"] = forecast_df["predicted_units_sold"]

        # rolling features
        forecast_df["rolling_mean_4"] = forecast_df[
            ["lag_1","lag_2","lag_3","lag_4"]
        ].mean(axis=1)

        forecast_df["rolling_mean_8"] = forecast_df[
            ["lag_1","lag_2","lag_3","lag_4","lag_8"]
        ].mean(axis=1)

        forecast_df["rolling_mean_12"] = forecast_df[
            ["lag_1","lag_2","lag_3","lag_4","lag_8","lag_12"]
        ].mean(axis=1)

    return forecasts