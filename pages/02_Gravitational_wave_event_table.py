import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from utilities import (
    get_gw_event_table_by_gwpy,
    convert_gps_to_utc
)


page_title = '重力波事件列表'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('藉由[GWpy](https://gwpy.github.io/docs/stable/)套件取得[重力波開放科學中心](https://www.gw-openscience.org/)提供的重力波事件列表，並能匯出CSV或JSON檔。')

with st.spinner('正在載入重力波事件列表，請稍候...'):
    gw_event_table = get_gw_event_table_by_gwpy()

time_format = st.radio(
    '切換表格中的時間格式', ['GPS時間系統', '世界協調時間(UTC)'], horizontal=True
)
if time_format == '世界協調時間(UTC)':
    gw_event_table = convert_gps_to_utc(gw_event_table)
else:
    gw_event_table = gw_event_table.rename(
        columns={'GPS': '觀測到緻密星體合併事件的時間(GPS時間系統)'}
    )
st.markdown('[GPS時間系統](https://gwpy.github.io/docs/stable/time/)是指從1980年1月6日午夜開始起算的秒數，重力波開放科學中心網站的「[UTC/GPS Time Converter](https://www.gw-openscience.org/gps/)」頁面有提供將GPS時間系統轉換成[世界協調時間(UTC)](https://zh.wikipedia.org/zh-tw/%E5%8D%8F%E8%B0%83%E4%B8%96%E7%95%8C%E6%97%B6)的功能。')

if st.sidebar.checkbox('去除欄位缺值的事件'):
    gw_event_table.dropna(inplace=True)

event_counts = len(gw_event_table)
events_per_row = st.sidebar.number_input(
    f'每頁顯示多少事件？ (共有{event_counts}筆事件)', min_value=1, max_value=event_counts, value=10
)

gb = GridOptionsBuilder.from_dataframe(gw_event_table)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=events_per_row)
gb.configure_column('事件名稱', pinned='left')
for col in gw_event_table.columns.values.tolist():
    gb.configure_column(col, suppressMovable=True, suppressMenu=True, skipHeaderOnAutoSize=True)

gridOptions = gb.build()
AgGrid(
    gw_event_table,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True,
    height=400,
    theme='balham'
)

output_format = st.sidebar.radio('匯出格式', ['CSV', 'JSON'], horizontal=True)
mime_dict = {
    'CSV': 'text/csv',
    'JSON': 'application/json'
}
output_data_dict = {
    'CSV': gw_event_table.to_csv(index=False),
    'JSON': gw_event_table.to_json(orient='records', force_ascii=False)
}
st.sidebar.download_button(
    label=f'將事件列表匯出成{output_format}檔',
    data=output_data_dict.get(output_format),
    file_name=f'gravitational_wave_event_table.{output_format.lower()}',
    mime=mime_dict.get(output_format)
)
