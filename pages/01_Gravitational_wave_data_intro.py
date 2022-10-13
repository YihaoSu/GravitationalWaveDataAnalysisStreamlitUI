import streamlit as st


page_title = '重力波資料簡介'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)

st.header('什麼是重力波?')
st.info('由黑洞、中子星或白矮星等體積小密度極大的[緻密星體](https://zh.wikipedia.org/zh-tw/%E8%87%B4%E5%AF%86%E6%98%9F)所組成的雙星系統，在雙星互繞合併的過程中，造成的彎曲時空變化會產生較容易被觀測到的漣漪：[重力波](https://zh.wikipedia.org/zh-tw/%E5%BC%95%E5%8A%9B%E6%B3%A2)，就像放在彈跳床上的兩個保齡球會造成彈跳床凹陷，且互繞時會讓彈跳床表面產生波動。')

st.header('可以從哪裡取得重力波的資料？')
st.subheader('1.重力波開放科學中心網站 ')
gwosc_intro = '''
[重力波開放科學中心](https://www.gw-openscience.org/)提供重力波觀測資料，以及資料分析的教學及軟體。
* Data相關頁面提供重力波事件列表，並且能直接從網站手動下載某個重力波事件的資料。
* Learning Resources相關頁面有影片、Jupyter Notebook型式的教材，以及歷年重力波資料分析工作坊的錄影。
* Software相關頁面有如何用API取得資料的說明文件，以及羅列許多用來取得、分析重力波觀測資料的Python套件。
'''
st.info(gwosc_intro)

st.subheader('2.GWOSC套件')
st.info('[GWOSC](https://gwosc.readthedocs.io/en/latest/)套件能取得重力波事件名稱清單，以及放在重力波開放科學中心網站上某個重力波事件的觀測資料檔案的下載連結。')
gwosc_example_code ='''
# 以GWOSC套件取得重力波事件名稱清單
from gwosc import datasets

gw_events = datasets.find_datasets(type='events')
'''
with st.expander('範例程式'):
	st.code(gwosc_example_code, language='python')

st.subheader('3.GWpy套件')
st.info('[GWpy](https://gwpy.github.io/docs/stable/)套件可以直接取得重力波觀測資料，並提供基本的重力波訊號處理(例如：過濾高低頻率雜訊、傅立葉頻譜分析、時頻分析)及資料視覺化功能。')
gwpy_example_code_event_list = '''
# 以GWpy套件取得重力波事件列表
from gwpy.table import EventTable

gw_events = EventTable.fetch_open_data('GWTC').to_pandas()
'''

gwpy_example_code_time_series = '''
# 用GWpy套件取得重力波時間序列觀測資料 
%matplotlib notebook
from gwpy.timeseries import TimeSeries

detector = 'H1' # 重力波偵測器代號，H1代表位於Hanford的LIGO偵測器，L1代表位於Livingston的LIGO偵測器
gw_event_gps_time = 1126259462.4 # GW150914事件的GPS時間
start_time = gw_event_gps_time - 15
end_time = gw_event_gps_time + 15

gw_event_data = TimeSeries.fetch_open_data(detector, start_time, end_time)
fig = gw_event_data.plot()
fig.show()
'''
with st.expander('範例程式'):
	st.code(gwpy_example_code_event_list, language='python')
	st.code(gwpy_example_code_time_series, language='python')
