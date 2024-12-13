import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

# Create a map
# Set initial position
m = folium.Map(location=[51.5, -0.1], zoom_start=10)  

# Enable export without the edit parameter
draw = Draw(export=True) 
draw.add_to(m)

# Show map
draw_result = st_folium(m, width=700, height=500, key="map1")

# Add an input box
wind_turbines = st.number_input('Please enter the number of wind turbines:', min_value=1, step=1)

if st.button("Submit"):
    if draw_result:
        #st.write("Debug draw_result data:", draw_result)

        # Attempt to extract from bounds
        if "bounds" in draw_result:
            bounds = draw_result["bounds"]
            lat_min = bounds["_southWest"]["lat"]
            lon_min = bounds["_southWest"]["lng"]
            lat_max = bounds["_northEast"]["lat"]
            lon_max = bounds["_northEast"]["lng"]

            st.write(f"Latitude and longitude ranges for selected areas:")
            st.write(f"The latitude range is from: {lat_min} to {lat_max}")
            st.write(f"The longitude range is from: {lon_min} to {lon_max}")

        # Attempt to extract from features
        elif "features" in draw_result and len(draw_result["features"]) > 0:
            feature = draw_result["features"][0]
            if "geometry" in feature and feature["geometry"]["type"] == "Polygon":
                coordinates = feature["geometry"]["coordinates"][0]
                lat_min = min([coord[1] for coord in coordinates])
                lat_max = max([coord[1] for coord in coordinates])
                lon_min = min([coord[0] for coord in coordinates])
                lon_max = max([coord[0] for coord in coordinates])

                st.write(f"Latitude and longitude ranges for selected areas:")
                st.write(f"The latitude range is from: {lat_min} to {lat_max}")
                st.write(f"The longitude range is from: {lon_min} to {lon_max}")
        else:
            st.write("No valid region data detected, please re-frame!")
    else:
        st.write("Please box an area first!")

