import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

# 创建地图
m = folium.Map(location=[51.5, -0.1], zoom_start=10)  # 设置初始位置
draw = Draw(export=True)  # 启用导出功能，不使用 edit 参数
draw.add_to(m)

# 显示地图
draw_result = st_folium(m, width=700, height=500, key="map1")  # 使用唯一键确保刷新

# 添加输入框
wind_turbines = st.number_input('请输入风力发电机的数量：', min_value=1, step=1)

if st.button("Submit"):
    if draw_result:
        #st.write("调试 draw_result 数据：", draw_result)

        # 尝试从 bounds 提取
        if "bounds" in draw_result:
            bounds = draw_result["bounds"]
            lat_min = bounds["_southWest"]["lat"]
            lon_min = bounds["_southWest"]["lng"]
            lat_max = bounds["_northEast"]["lat"]
            lon_max = bounds["_northEast"]["lng"]

            st.write(f"选定区域的经纬度范围：")
            st.write(f"纬度范围: {lat_min} 到 {lat_max}")
            st.write(f"经度范围: {lon_min} 到 {lon_max}")

        # 尝试从 features 提取
        elif "features" in draw_result and len(draw_result["features"]) > 0:
            feature = draw_result["features"][0]
            if "geometry" in feature and feature["geometry"]["type"] == "Polygon":
                coordinates = feature["geometry"]["coordinates"][0]
                lat_min = min([coord[1] for coord in coordinates])
                lat_max = max([coord[1] for coord in coordinates])
                lon_min = min([coord[0] for coord in coordinates])
                lon_max = max([coord[0] for coord in coordinates])

                st.write(f"选定区域的经纬度范围：")
                st.write(f"纬度范围: {lat_min} 到 {lat_max}")
                st.write(f"经度范围: {lon_min} 到 {lon_max}")
        else:
            st.write("未检测到有效区域数据，请重新框选！")
    else:
        st.write("请先框选一个区域！")

