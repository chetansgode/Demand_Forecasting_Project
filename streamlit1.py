import streamlit as st 
import requests
from data_created.unique_store_sku import sku_list,store_list


#request_url="http://127.0.0.1:8000/forecast" this is fastapi
request_url="http://fastapi:8000/forecast"  #for docker
st.title('forcast next number of week demand data')

n_weeks=st.number_input('how many next week data do you want?',value=12)
store_id=st.selectbox('select store_id where data want?',options=store_list,index=0)
sku_id=st.selectbox('select sku_id where data want?',options=sku_list,index=0)

st.text(f"you select store_id -{store_id} and sku_id -{sku_id} and no of week -{n_weeks}")

if st.button(f'forcasting next {n_weeks} week'):
    
    input_data = {
        "n_weeks": n_weeks,
        "store_id": store_id,
        "sku_id": sku_id,
        
    }

    try:
       response= requests.post(request_url,json=input_data)
       result=response.json()
       if response.status_code==200:
           prediction = result.get("forecast")
           #show data frame
           import pandas as pd
           df = pd.DataFrame(prediction)
           df.index+=1
           
           st.success(f'Forecating {n_weeks} no of week sales   **{st.dataframe(df)}**')
       else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")
