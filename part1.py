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

@st.cache_resource
def cache3_loc_list():
    loc_list_lun = []
    return loc_list_lun
loc_list_lunch = cache3_loc_list()


# front_end
image = st.image("trip_image.jpg")
title = st.title("TripOpt_卒業研究")
creater = st.text("Yuki Hiramatsu")


#　出発地_目的地
with st.form("出発地_目的地",clear_on_submit=False):
    loc_start = st.text_input("出発地", placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    loc_goal = st.text_input("目的地", placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    time_start_goal = st.slider(
    '出発到着予定時刻',
    datetime.time(5, 0), datetime.time(23,0), (datetime.time(9, 45), datetime.time(18, 15)),
    step=datetime.timedelta(minutes=15),
    format=("Ah時mm分")
    )

    go_button = st.form_submit_button("確定")
    if go_button:
        loc_list_start_goal.clear()
        split_url1 , zahyo1 = url_org(loc_start)
        loc_list_start_goal.append([urllib.parse.unquote(split_url1[5]),float(zahyo1[0].split("@")[1]),float(zahyo1[1])])
        split_url2 , zahyo2 = url_org(loc_goal)
        loc_list_start_goal.append([urllib.parse.unquote(split_url2[5]),float(zahyo2[0].split("@")[1]),float(zahyo2[1])])
        location_start_goal = pd.DataFrame(loc_list_start_goal, columns=["地名","latitude","longitude"])
        
        st.session_state['form1_1'] = time_start_goal
        st.session_state['form1_2'] = location_start_goal

try:
    st.dataframe(st.session_state.form1_2,height=110)
    # folium 出発地_目的地
    ave_lat1 = st.session_state.form1_2["latitude"].sum()/2
    ave_lon1 = st.session_state.form1_2["longitude"].sum()/2
    m_start_goal = folium.Map(
        location=[ave_lat1, ave_lon1],
        zoom_start=7
    )
    for i, row in st.session_state.form1_2.iterrows():
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
except AttributeError:
    pass


# 昼ご飯選択するかしないか
with st.form("ランチの場所を選択する",clear_on_submit=False):
    lunch_Y_N = st.radio("ランチの場所(複数候補可能)", ["指定する","指定しない"],index=1,horizontal=True)
    confirm_button = st.form_submit_button("確定")
    if lunch_Y_N == "指定する":
        loc_lunch = st.text_input("場所", placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
        if confirm_button or lunch_Y_N == "指定する":
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                lunch_submit_button = st.form_submit_button("追加")
                if lunch_submit_button:
                    split_url4 , zahyo4 = url_org(loc_lunch)
                    loc_list_lunch.append([urllib.parse.unquote(split_url4[5]),float(zahyo4[0].split("@")[1]),float(zahyo4[1])])
                    location_lunch = pd.DataFrame(loc_list_lunch, columns=["地名","latitude","longitude"])
                    
                    st.session_state["form2_1"] = location_lunch
                
            with col2_2:
                lunch_reset_button = st.form_submit_button("リセット")
                if lunch_reset_button:
                    loc_list_lunch.clear()
                    location_lunch = ["Lunch location not selected."]
                    
                    st.session_state['form2_1'] = location_lunch
                    st.session_state["form2_2"] = lunch_Y_N

try:
    st.dataframe(st.session_state.form2_1,height = 110)
except:
    pass

try:
    for i, row in st.session_state.form2_1.iterrows():
    # ポップアップの作成
        pop=f"{row['地名']}<br> 緯度…{row['latitude']:,}<br> 経度…{row['longitude']:,}"
        folium.Marker(
            # 緯度と経度を指定
            location=[row['latitude'], row['longitude']],
            # ポップアップの指定
            popup=folium.Popup(pop, max_width=300),
            # アイコンの指定(アイコン、色)
            icon=folium.Icon(color="orange",icon="cutlery")
        ).add_to(m_start_goal)
except:
    pass


#　行きたいところ        
with st.form("行きたいところ",clear_on_submit=False):
    location =  st.text_input('行きたいところ', placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    col3_1, col3_2 = st.columns(2)
    with col3_1:
        submit_button = st.form_submit_button("追加")
        if submit_button:
            split_url3 , zahyo3 = url_org(location)
            loc_list_where.append([urllib.parse.unquote(split_url3[5]),float(zahyo3[0].split("@")[1]),float(zahyo3[1])])
            location_time = pd.DataFrame(loc_list_where, columns=["地名","latitude","longitude"])
            
            st.session_state['form3_1']= location_time
            
    with col3_2:
        reset_button = st.form_submit_button("リセット")
        if reset_button:
            loc_list_where.clear()
            location_time = ["No data is included."]
            
            st.session_state['form3_1']= location_time

try:
    # folium 出発地_目的地_行きたいところ

    for i, row in st.session_state.form3_1.iterrows():
    # ポップアップの作成
        pop=f"{row['地名']}<br> 緯度…{row['latitude']:,}<br> 経度…{row['longitude']:,}"
        folium.Marker(
            # 緯度と経度を指定
            location=[row['latitude'], row['longitude']],
            # ポップアップの指定
            popup=folium.Popup(pop, max_width=300),
            # アイコンの指定(アイコン、色)
            icon=folium.Icon(color="red",icon="glyphicon glyphicon-bookmark")
        ).add_to(m_start_goal)
    st.dataframe(st.session_state.form3_1,height = 200)
except:
    pass

try:
    st_folium(m_start_goal, width=480, height=320)
except:
    pass