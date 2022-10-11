import streamlit as st
from gwpy.time import from_gps

from utilities import (
    get_gw_event_table_by_gwpy,
    get_gw_event_data
)


def plot_gw_event_time_series(
    gw_event_data, gw_event_name, gw_detector, gw_event_gps_time
):
    fig = gw_event_data.plot()
    ax = fig.gca()
    ax.set_epoch(gw_event_gps_time)
    ax.set_title(f'{gw_detector} strain data around {gw_event_name}')
    ax.set_ylabel('Gravitational-wave amplitude [strain]')
    ax.axvline(gw_event_gps_time, color='red', linestyle='--')

    return st.pyplot(fig)


page_title = '重力波資料分析'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('選擇重力波事件，以呈現該事件的時間序列觀測資料，並能操作基本的資料處理及分析。')

with st.spinner('正在載入重力波事件列表，請稍候...'):
    gw_event_table = get_gw_event_table_by_gwpy()

gw_event_list = gw_event_table['事件名稱'].to_list()
gw_event_name = st.sidebar.selectbox('選擇重力波事件', gw_event_table)
gw_event = gw_event_table[
    gw_event_table['事件名稱'] == gw_event_name].iloc[0]
gw_event_gps_time = gw_event['GPS']
gw_event_utc_time = from_gps(gw_event_gps_time).strftime('%Y年%m月%d日%H點%M分%S秒')
mass1 = gw_event['緻密星體1的質量(單位：太陽質量)']
mass2 = gw_event['緻密星體2的質量(單位：太陽質量)']

gw_detector_dict = {
    'LIGO-Hanford': 'H1',
    'LIGO-Livingston': 'L1'

}
gw_detector = st.sidebar.selectbox(
    '選擇重力波偵測器', list(gw_detector_dict.keys())
)

with st.spinner(f'正在載入{gw_event_name}重力波事件的觀測資料，請稍候...'):
    gw_event_data = get_gw_event_data(
        gw_event_gps_time, gw_detector_dict.get(gw_detector)
)

st.subheader(f'{gw_event_name}重力波事件發生前後15秒的觀測資料')
st.success(f'{gw_event_name}是由兩個質量分別比太陽大上{mass1}及{mass2}倍的[緻密星體](https://zh.wikipedia.org/zh-tw/%E8%87%B4%E5%AF%86%E6%98%9F)合併所產生的重力波事件，於{gw_event_utc_time}(UTC)被觀測到。')
plot_gw_event_time_series(
    gw_event_data, gw_event_name, gw_detector, gw_event_gps_time
)
