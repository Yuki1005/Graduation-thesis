import streamlit as st
import pandas as pd
import urllib.parse

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

title = st.title("TripOpt")

#　出発地点_目的地
with st.form("出発地点_目的地"):
    location_start = st.text_input("出発地点", placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    location_goal = st.text_input("目的地", placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    go_button = st.form_submit_button("確定")
    if go_button:
        loc_list_start_goal.clear()
        split_url , zahyo = url_org(location_start)
        loc_list_start_goal.append([urllib.parse.unquote(split_url[5]),float(zahyo[0].split("@")[1]),float(zahyo[1])])
        location_start_goal = pd.DataFrame(loc_list_start_goal, columns=["地名","latitude","longitude"])
        split_url , zahyo = url_org(location_goal)
        loc_list_start_goal.append([urllib.parse.unquote(split_url[5]),float(zahyo[0].split("@")[1]),float(zahyo[1])])
        location_start_goal = pd.DataFrame(loc_list_start_goal, columns=["地名","latitude","longitude"])
        
        st.dataframe(location_start_goal,height = 110)
    
#　行きたいところ        
with st.form("行きたいところ",clear_on_submit=True):
    location =  st.text_input('行きたいところ', placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    col1_2, col2_2 = st.columns(2)
    with col1_2:
        submit_button = st.form_submit_button("追加")
        if submit_button:
            split_url , zahyo = url_org(location)
            loc_list_where.append([urllib.parse.unquote(split_url[5]),float(zahyo[0].split("@")[1]),float(zahyo[1])])
            location_time = pd.DataFrame(loc_list_where, columns=["地名","latitude","longitude"])
            
            st.experimental_set_query_params()
            st.dataframe(location_time,height = 200)
    with col2_2:
        reset_button = st.form_submit_button("リセット")
        if reset_button:
            loc_list_where.clear()