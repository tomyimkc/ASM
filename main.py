from cProfile import label
from tracemalloc import start
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import statistics as stat
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode

# import ib_data
# from Stock_Data import get_specific_data
# from plot_df import plot
# from Volatility_sim import check_history

profile_df=pd.read_csv(f'{path_data}core{sep}Profile_Summary.csv')

def sim(df,start_index,end_index):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        figure,axis = plt.subplots(4,1,figsize=(9,9))
                        
                        # st.dataframe(df)
                        x_date_array=[datetime.datetime.strptime(d,"%Y-%m-%d %H:%M:%S") for d in df['date']]
                        # st.write(x_date_array)
                        x_array=[]
                        open_array=[]
                        high_array=[]
                        low_array=[]
                        close_array=[]
                        HL_array=[]
                        volume_array=[]
                        B_array=[]
                        S_array=[]
                        T_array=[]
                        sd_array=[]
                        mean_array=[]

                        for i in range(start_index,end_index):
                    
                            x_array.append(x_date_array[i-start_index])
                            open_array.append(df['open'][i])
                            high_array.append(df['high'][i])
                            low_array.append(df['low'][i])
                            close_array.append(df['close'][i])
                            HL_array.append(df['HL'][i])
                            volume_array.append(df['volume'][i])
                            if i >start_index:
                                sd=stat.stdev(HL_array[-60:])
                                sd_array.append(sd)
                                mean=stat.mean(HL_array[-60:])
                                mean_array.append(mean)
                            else:
                                sd=df['HL'][i]*0.341
                                sd_array.append(sd)
                                mean=df['HL'][i]/2
                                mean_array.append(mean)


                            print ('mean:',mean,'sd:',sd)

                            plt.cla()
                            axis[0].plot(x_array, open_array,label='open'if         i == start else "",color='g')
                            axis[0].plot(x_array, high_array,label='high'if         i == start else "",color='r')
                            axis[0].plot(x_array, low_array,label='low'if i         == start else "",color='m')
                            axis[0].plot(x_array, close_array,      label='close'if i == start else "",color='b')
                            axis[1].plot(x_array, HL_array,label='HL'if i ==        start else "",color='r')
                            axis[2].plot(x_array, mean_array,label='mean'if         i == start else "",color='r')
                            axis[2].plot(x_array, sd_array,label='sd'if i ==        start else "",color='g')
                            axis[3].plot(x_array, volume_array,     label='volume',color='g')

                            # plt.title(str(i))
                            # axis[0].legend()
                            # axis[1].legend()
                            # axis[2].legend()
                            # axis[3].legend()


                        mean_mean=stat.mean(mean_array)
                        mean_sd=stat.stdev(mean_array)
                        sd_mean=stat.mean(sd_array)
                        sd_sd=stat.stdev(sd_array)
                        volume_mean=stat.mean(volume_array)
                        volume_sd=stat.stdev(volume_array)
                        st.pyplot(figure)
                        st.write('The mean of mean_array=',mean_mean)
                        st.write('The sd of mean_array=',mean_sd)
                        st.write('The mean of sd_array=',sd_mean)
                        st.write('The sd of sd_array=',sd_sd)
                        st.write('The mean of volume_array=',volume_mean)
                        st.write('The sd of volume_array=',volume_sd)
                        sim_occur_in_HL_time=sum(mean_mean+sd_mean < i for i in HL_array)
                        st.write("Time of Simulation Range within HL frame",sim_occur_in_HL_time)
                        # count the times of uptrending with range greater than sim time

def nice_grid(df):
    

    gb = GridOptionsBuilder.from_dataframe(df)
    # enables pivoting on all columns, however i'd need to  change ag grid to allow export of pivoted/grouped data,  however it select/filters groups
    gb.configure_default_column(enablePivot=True,   enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple",   use_checkbox=True)
    gb.configure_side_bar()  # side_bar is clearly a typo :)    should by sidebar
    gridOptions = gb.build()

    

    response = AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
    )

    # st.table(df)
 

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
    ticker_array=profile_df['Ticker'].tolist()
    ticker=st.selectbox('Choose your profile ticker',ticker_array)
    checkbox_status=st.checkbox('Check Ticker')
    if not ticker == '' and checkbox_status:
        
        with st.expander("DF detail:"):
            select_df_status=st.checkbox('Simulation: volatility')
            if select_df_status:
                history_df=pd.read_csv(f"{path_data}sim{sep}{ticker}_history.csv")
                all_df_status=st.checkbox('All Data inside DF')
                if all_df_status:
                    nice_grid(history_df)
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
            