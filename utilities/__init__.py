import streamlit as st
from gwpy.table import EventTable
from gwpy.time import from_gps


@st.experimental_memo(ttl=86400, show_spinner=False)
def get_gw_event_table_by_gwpy():
    gw_event_table = EventTable.fetch_open_data('GWTC').to_pandas()
    gw_event_table = gw_event_table[
        [
            'commonName', 'GPS', 'mass_1_source', 'mass_2_source', 'luminosity_distance'
        ]
    ]
    gw_event_table = gw_event_table.rename(
        columns={
            'commonName': '事件名稱',
            'mass_1_source': '緻密星體1的質量(單位：太陽質量)',
            'mass_2_source': '緻密星體2的質量(單位：太陽質量)',
            'luminosity_distance': '與地球的距離(單位：百萬秒差距)',
        }
    )
    gw_event_table.sort_values(by='GPS', inplace=True, ignore_index=True)

    return gw_event_table


def convert_gps_to_utc(gw_event_table):
    gw_event_table['GPS'] = gw_event_table['GPS'].apply(
        lambda x: from_gps(x).strftime('%Y-%m-%d %H:%M:%S')
    )
    gw_event_table = gw_event_table.rename(
        columns={'GPS': '觀測到緻密星體合併事件的時間(UTC)'}
    )

    return gw_event_table
