import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from utilities import (
    get_gw_event_table_by_gwpy
)


page_title = '重力波事件列表'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('藉由[GWpy](https://gwpy.github.io/docs/stable/)套件取得[重力波開放科學中心](https://www.gw-openscience.org/)提供的重力波事件列表。')

with st.spinner('正在載入重力波事件列表，請稍候...'):
    gw_event_table = get_gw_event_table_by_gwpy()


gb = GridOptionsBuilder.from_dataframe(gw_event_table)
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
