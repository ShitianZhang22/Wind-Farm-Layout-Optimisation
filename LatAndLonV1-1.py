import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from Optimiser.main import optimisation
from Transfer import *

st.markdown('# Wind Farm Layout Optimisation')

# Create a map
# Set initial position
# m = folium.Map(location=[51.5, -0.1], zoom_start=10)  # This is London
m = folium.Map(location=[55.674099775230026, -4.271278381347657], zoom_start=12)  # This is Whitelee wind farm

# Initialise session state for wind turbine locations
if 'wt_pos' not in st.session_state:
    st.session_state['wt_pos'] = []
# Initialise the wind farm site boundaries
if 'site' not in st.session_state:
    st.session_state['site'] = [[55.6350646, -4.3633451], [55.7140006, -4.1843088]]

# Enable export without the edit parameter
# Draw(export=True).add_to(m)

# on clicking the submit button
if st.button("Submit"):
    st.write('wind turbine number:{}'.format(st.session_state['wt']))

    solution = optimisation()
    solution = gene_to_pos(solution)
    # solution = gene_to_pos(None)
    st.session_state['wt_pos'] = solution

    # for i in range(solution.shape[0]):
    #     print(solution[i])
    #     st.session_state['wind turbines'].append(
    #         folium.Marker(solution[i], icon=folium.Icon(icon='info', prefix='fa', icon_color='white'))
    #     )

    # The following part is for site selection, and is closed at the moment.
    # if draw_result:
    #     st.write("Debug draw_result data:", draw_result)
    #     print(draw_result)
    #
    #     # Attempt to extract from bounds
    #     if "bounds" in draw_result:
    #         bounds = draw_result["bounds"]
    #         lat_min = bounds["_southWest"]["lat"]
    #         lon_min = bounds["_southWest"]["lng"]
    #         lat_max = bounds["_northEast"]["lat"]
    #         lon_max = bounds["_northEast"]["lng"]
    #
    #         st.write(f"Latitude and longitude ranges for selected areas:")
    #         st.write(f"The latitude range is from: {lat_min} to {lat_max}")
    #         st.write(f"The longitude range is from: {lon_min} to {lon_max}")
    #
    #     # Attempt to extract from features
    #     elif "features" in draw_result and len(draw_result["features"]) > 0:
    #         feature = draw_result["features"][0]
    #         if "geometry" in feature and feature["geometry"]["type"] == "Polygon":
    #             coordinates = feature["geometry"]["coordinates"][0]
    #             lat_min = min([coord[1] for coord in coordinates])
    #             lat_max = max([coord[1] for coord in coordinates])
    #             lon_min = min([coord[0] for coord in coordinates])
    #             lon_max = max([coord[0] for coord in coordinates])
    #
    #             st.write(f"Latitude and longitude ranges for selected areas:")
    #             st.write(f"The latitude range is from: {lat_min} to {lat_max}")
    #             st.write(f"The longitude range is from: {lon_min} to {lon_max}")
    #     else:
    #         st.write("No valid region data detected, please re-frame!")
    # else:
    #     st.write("Please box an area first!")

# Add an input box
st.number_input('Please enter the number of wind turbines:', min_value=1, step=1, key='wt')

fg = folium.FeatureGroup(name='Wind_Turbines')
for pos in st.session_state['wt_pos']:
    fg.add_child(folium.Marker(pos))
fg.add_child(folium.Rectangle(st.session_state['site']))


# Show map
st_folium(m, feature_group_to_add=fg, width=700, height=500, key="map1")
st.write(st.session_state)
