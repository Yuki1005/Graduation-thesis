import streamlit as st
import pandas as pd
import urllib.parse

# 関数まとめ

def url_org(loc_list):
    url_data = location
    split_url = url_data.split("/")
    zahyo = split_url[6].split(",")
    return split_url,zahyo

# streamlit global関数

@st.cache_resource
def cache_loc_list():
    loc_list = []
    return loc_list
loc_list = cache_loc_list()

# front_end

image = st.image("trip_image.jpg")

title = st.title("TriOpt")

        
with st.form("行きたいところ",clear_on_submit=True):
    location =  st.text_input('行きたいところ', placeholder='GoogleMap_URL', help='GoogleMapのURLを使用すること')
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.form_submit_button("追加")
        if submit_button:
            split_url , zahyo = url_org(loc_list)
            loc_list.append([urllib.parse.unquote(split_url[5]),float(zahyo[0].split("@")[1]),float(zahyo[1])])
            location_time = pd.DataFrame(loc_list, columns=["地名","latitude","longitude"])
            
            st.experimental_set_query_params()
            st.dataframe(location_time,height = 200)
    with col2:
        reset_button = st.form_submit_button("リセット")
        if reset_button:
            loc_list.clear()