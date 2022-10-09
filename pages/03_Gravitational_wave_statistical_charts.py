import streamlit as st
import plotly.express as px

from utilities import get_gw_event_table_by_gwpy


def plot_histogram(gw_event_table, column_name):
	fig = px.histogram(
        gw_event_table, x=column_name, nbins=20,
    )
	fig.update_layout(
		yaxis_title='數量'
	)

	return st.plotly_chart(fig, use_container_width=True)


page_title = '重力波事件統計'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)
st.info('將重力波事件列表中的資料以統計圖呈現。')

with st.spinner('正在載入重力波事件列表，請稍候...'):
    gw_event_table = get_gw_event_table_by_gwpy()
    gw_event_table.dropna(inplace=True)

col1, col2 = st.columns(2)
with col1:
    plot_histogram(gw_event_table, '緻密星體1的質量(單位：太陽質量)')
with col2:
    plot_histogram(gw_event_table, '緻密星體2的質量(單位：太陽質量)')


fig = px.scatter(
    gw_event_table,
    x='緻密星體1的質量(單位：太陽質量)',
    y='緻密星體2的質量(單位：太陽質量)',
    size='緻密星體合併後的質量(單位：太陽質量)',
    color='緻密星體合併後的質量(單位：太陽質量)',
    hover_name='事件名稱',
    range_x=[0, 120], range_y=[0, 120]
)
fig.add_hline(
    y=3, line_width=3, line_dash='dash', line_color='green',
    annotation_text='中子星質量上界線：3倍太陽質量',
)
fig.add_vline(
    x=3, line_width=3, line_dash='dash', line_color='green',
    annotation_text='中子星質量上界線：3倍太陽質量',
)
st.plotly_chart(fig, use_container_width=True)
