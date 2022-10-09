import streamlit as st


page_title = '重力波資料分析app'
st.set_page_config(page_title=page_title, page_icon=':star', layout='wide')
st.title(page_title)

st.info('此Web App是以重力波資料分析作為範例，用來教學及推廣公民科學，由[蘇羿豪](https://astrobackhacker.tw/)基於[Streamlit](https://streamlit.io/)開發，[程式碼](https://github.com/YihaoSu/GravitationalWaveDataAnalysisStreamlitUI)以MIT授權條款開源，並將開發過程紀錄在2022 iThome鐵人賽的系列文章「[跟著黑蛋用Streamlit速成天文資料分析Web App](https://ithelp.ithome.com.tw/users/20103436/ironman/5820)」中。')
st.markdown('* Gravitational wave event table頁面呈現從[重力波開放科學中心](https://www.gw-openscience.org/)取得的重力波事件列表，並提供匯出CSV或JSON檔的功能。')
st.markdown('* Gravitational wave statistical charts頁面呈現重力波事件的統計圖。')
