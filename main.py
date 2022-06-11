from cProfile import label
from tracemalloc import start
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import statistics as stat

# import ib_data
# from Stock_Data import get_specific_data
# from plot_df import plot
# from Volatility_sim import check_history


def convert(date_time):
    format='%Y-%m-%d'
    datetime_str=datetime.datetime.strptime(str(date_time),format)

    #end_time='20220219 04:00:00'
    new_time=datetime_str+datetime.timedelta(days=1,hours=4)
    # st.write(new_time)

    ib_time=new_time.strftime('%Y%m%d %H:%M:%S')
    # st.write(ib_time)
    
    return ib_time, new_time


st.title("Auto Stock Management (ASM)")
st.header("Made by Tom Yim")
st.write("Input Ticker and check its stat")
st.sidebar.title("ASM")
st.sidebar.subheader("By Tom Yim")
option=st.sidebar.selectbox("Function:",("Index","Data Check","wallstreetbets"))


if option=="Index":
    # ticker="TSLA"
    st.subheader("This is the Index page")
    # st.subheader(ticker)
    # df=pd.read_csv(f"{path_data}Sim{sep}{ticker}_history.csv")
    # st.dataframe(df)
elif option == "Data Check":
    ticker=st.text_input("Text Box",max_chars=5)
    ticker_array=['TSLA','AMD']
    ticker=st.selectbox('Choose your profile ticker',ticker_array)
    checkbox_status=st.checkbox('Check Ticker')
    if not ticker == '' and checkbox_status:
        
        with st.expander("DF detail:"):
            select_df_status=st.checkbox('Simulation: volatility')
            if select_df_status:
                all_df_status=st.checkbox('All Data inside DF')
                specific_df_status=st.checkbox('Simulation')
                if specific_df_status:
                    simulation_range_status=st.checkbox('Simulation between a range of data')
                    if simulation_range_status:
                        check_duration=st.slider("Simulation Days Duration:",0,29)
                        start_date, end_date = st.select_slider('Select a range of date',options=range(0,30),value=(0,29))
                        st.write(start_date,end_date)
                        start_place=-(start_date+1)*390
                        end_place=start_place+390*(end_date-start_date)
                    # st.write(check_duration)
                        select_df=history_df.iloc[-(check_duration+1)*390:]
                        start_index=(29-check_duration)*390
                        end_index=start_index+390
                    # st.write(start_index)
                    # st.write(select_df['open'][start_index])
                        nice_grid(select_df)

                    target_checkbox=st.checkbox('Simulation of a target date')
                    # target
                    if target_checkbox:
                        date=st.date_input(f"{ticker} Preformance at:")
                    # st.write(f'{ticker} preform at',date)
                        ib_check_time=convert(date)
                    # st.write(ib_check_time[0])
                    # st.write(ib_check_time[1])
                        end_time=ib_check_time[1]-datetime.timedelta(minutes=1)
                    # st.write(end_time)
                        row_number=history_df[history_df['date']==str(end_time)].index
                    # st.write(row_number[0])
                        start_index=row_number[0]-389
                        end_index=row_number[0]+1
                        target_df=history_df.iloc[start_index:end_index]
                        target_status=st.checkbox('Target Date DF')
                        if target_status:
                            t_status=st.checkbox('Show DF')
                            if t_status:
                                nice_grid(target_df)
                            # st.dataframe(target_df)
                            start = st.checkbox('Start Sim')
                    # sim(target_df)
                            if start:
                                sim(target_df,start_index,end_index)
            