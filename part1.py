import streamlit as st
import pandas as pd
import urllib.parse
import folium
from streamlit_folium import st_folium
import datetime



# 関数まとめ
def url_org(url_google):
    url_data = url_google
    split_url = url_data.split("/")
    zahyo = split_url[6].split(",")
    return split_url,zahyo


# streamlit global関数
@st.cache_resource
def cache1_loc_list():
    loc_list_ikitai = []
    return loc_list_ikitai
loc_list_where = cache1_loc_list()

@st.cache_resource
def cache2_loc_list():
    loc_list_az = []
    return loc_list_az
loc_list_start_goal = cache2_loc_list()


# front_end
image = st.image("trip_image.jpg")
title = st.title("TripOpt_卒業研究")
creater = st.text("Yuki Hiramatsu")


#　出発地点_目的地
with st.form("出発地点_目的地",clear_on_submit=False):
    loc_start = st.text_input("出発地点", placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    time_start = st.time_input("出発時刻", datetime.time(10, 00))
    loc_goal = st.text_input("目的地", placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    time_goal = st.time_input("到着時刻", datetime.time(18, 00))

    go_button = st.form_submit_button("確定")
    if go_button:
        loc_list_start_goal.clear()
        split_url1 , zahyo1 = url_org(loc_start)
        loc_list_start_goal.append([urllib.parse.unquote(split_url1[5]),float(zahyo1[0].split("@")[1]),float(zahyo1[1])])
        location_start_goal = pd.DataFrame(loc_list_start_goal, columns=["地名","latitude","longitude"])
        split_url2 , zahyo2 = url_org(loc_goal)
        loc_list_start_goal.append([urllib.parse.unquote(split_url2[5]),float(zahyo2[0].split("@")[1]),float(zahyo2[1])])
        location_start_goal = pd.DataFrame(loc_list_start_goal, columns=["地名","latitude","longitude"])
            
        st.session_state['form1']= location_start_goal

try:
    # folium 出発地点_目的地
    ave_lat1 = st.session_state.form1["latitude"].sum()/2
    ave_lon1 = st.session_state.form1["longitude"].sum()/2
    m_start_goal = folium.Map(
        location=[ave_lat1, ave_lon1],
        zoom_start=6
    )
    for i, row in st.session_state.form1.iterrows():
    # ポップアップの作成
        pop=f"{row['地名']}<br> 緯度…{row['latitude']:,}<br> 経度…{row['longitude']:,}"
        folium.Marker(
            # 緯度と経度を指定
            location=[row['latitude'], row['longitude']],
            # ポップアップの指定
            popup=folium.Popup(pop, max_width=300),
            # アイコンの指定(アイコン、色)
            icon=folium.Icon(icon_color="white", color="blue")
        ).add_to(m_start_goal)
    st_folium(m_start_goal, width=480, height=320)
    st.dataframe(st.session_state.form1,height=110)
except AttributeError:
    pass


#　行きたいところ        
with st.form("行きたいところ",clear_on_submit=False):
    location =  st.text_input('行きたいところ', placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    col1_2, col2_2 = st.columns(2)
    with col1_2:
        submit_button = st.form_submit_button("追加")
        if submit_button:
            split_url3 , zahyo3 = url_org(location)
            loc_list_where.append([urllib.parse.unquote(split_url3[5]),float(zahyo3[0].split("@")[1]),float(zahyo3[1])])
            location_time = pd.DataFrame(loc_list_where, columns=["地名","latitude","longitude"])
            st.session_state['form2']= location_time
    with col2_2:
        reset_button = st.form_submit_button("リセット")
        if reset_button:
            loc_list_where.clear()
            location_time = ["No data is included."]
            st.session_state['form2']= location_time

try:
    st.dataframe(st.session_state.form2,height = 200)
except:
    pass