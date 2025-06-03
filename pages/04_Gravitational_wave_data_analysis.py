import streamlit as st
from gwpy.time import from_gps
from gwpy.signal import filter_design

from utilities import (
    get_gw_event_table_by_gwpy,
    get_gw_event_data
)


def filter_signal_by_bandpass(gw_event_data, freq_low_limit, freq_high_limit):
    # 參考文件：https://gwpy.github.io/docs/stable/examples/signal/gw150914/
    bp = filter_design.bandpass(
        freq_low_limit, freq_high_limit, gw_event_data.sample_rate
    )
    notches = [filter_design.notch(
        line, gw_event_data.sample_rate) for line in (60, 120, 180)]
    zpk = filter_design.concatenate_zpks(bp, *notches)
    filtered_gw_event_data = gw_event_data.filter(zpk, filtfilt=True)

    return filtered_gw_event_data


def plot_gw_event_time_series(
    gw_event_data, gw_event_name, gw_detector, gw_event_gps_time, dt
):
    fig = gw_event_data.crop(gw_event_gps_time - dt, gw_event_gps_time + dt).plot()
    ax = fig.gca()
    ax.set_epoch(gw_event_gps_time)
    ax.set_title(f'{gw_detector} data around {gw_event_name}')
    ax.set_ylabel('Gravitational-wave amplitude')
    ax.axvline(gw_event_gps_time, color='red', linestyle='--')

    return st.pyplot(fig)


def plot_qspecgram(qspecgram, gw_event_gps_time):
    fig = qspecgram.plot()
    ax = fig.gca()
    ax.set_xscale('seconds')
    ax.set_yscale('log')
    ax.set_epoch(gw_event_gps_time)
    ax.set_ylabel('Frequency [Hz]')
    ax.grid(True, axis='y', which='both')
    fig.colorbar(ax.images[0], label='Normalized energy')

    return st.pyplot(fig)


page_title = '重力波資料分析'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('選擇重力波事件，以呈現該事件的時間序列觀測資料，並能操作基本的資料處理及分析。')

with st.spinner('正在載入重力波事件列表，請稍候...'):
    gw_event_table = get_gw_event_table_by_gwpy()

gw_event_list = gw_event_table['事件名稱'].to_list()
gw_event_name = st.sidebar.selectbox('選擇重力波事件', gw_event_list)
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
dt = st.sidebar.slider('觀測資料要涵蓋事件前後幾秒？', 0.1, 15.0, 3.0, step=0.1)

with st.spinner(f'正在載入{gw_event_name}重力波事件的觀測資料，請稍候...'):
    gw_event_data = get_gw_event_data(
        gw_detector_dict.get(gw_detector), gw_event_gps_time
)

st.header(f'{gw_event_name}重力波事件發生前後{dt}秒的觀測資料')
st.success(f'{gw_event_name}是由兩個質量分別比太陽大上{mass1}及{mass2}倍的[緻密星體](https://zh.wikipedia.org/zh-tw/%E8%87%B4%E5%AF%86%E6%98%9F)合併所產生的重力波事件，於{gw_event_utc_time}(UTC)被觀測到。')
st.subheader('包含雜訊的原始資料')
plot_gw_event_time_series(
    gw_event_data, gw_event_name, gw_detector, gw_event_gps_time, dt
)

freq_low_limit = st.sidebar.number_input('要濾除頻率為多少赫茲以下的低頻雜訊？', value=50)
freq_high_limit = st.sidebar.number_input('要濾除頻率為多少赫茲以上的高頻雜訊？', value=250)

filtered_gw_event_data = filter_signal_by_bandpass(
    gw_event_data, freq_low_limit, freq_high_limit
)

st.subheader('濾除雜訊後的資料')
plot_gw_event_time_series(
    filtered_gw_event_data, gw_event_name, gw_detector, gw_event_gps_time, dt
)

st.subheader('藉由Q-transform分析重力波訊號的頻率及強度隨時間的變化')
with st.expander('什麼是Q-transform?'):
    st.markdown('[Q-transform](https://zh.wikipedia.org/zh-tw/%E5%B8%B8%E6%95%B8Q%E8%BD%89%E6%8F%9B)是一種針對訊號的[時頻分析](https://zh.wikipedia.org/zh-tw/%E6%99%82%E9%A0%BB%E5%88%86%E6%9E%90)方法，它能將一維的時間序列訊號，轉換成一種稱作[時頻譜](https://zh.wikipedia.org/zh-tw/%E6%97%B6%E9%A2%91%E8%B0%B1)的二維圖，橫軸為時間，縱軸為頻率，顏色深淺代表訊號的強弱，同時呈現訊號的頻率及強度隨時間的變化。')

qcenter = st.sidebar.slider('Q-transform的Q值要設定多少？', 5, 120, 5)
qrange = (int(qcenter * 0.8), int(qcenter * 1.2))
qspecgram = gw_event_data.q_transform(
    outseg=(gw_event_gps_time - dt, gw_event_gps_time + dt),
    qrange=qrange
)
plot_qspecgram(qspecgram, gw_event_gps_time)
