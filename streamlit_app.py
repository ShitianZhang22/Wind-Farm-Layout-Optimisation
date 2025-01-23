import streamlit as st
import folium
from folium.plugins import MousePosition
from streamlit_folium import st_folium
import streamlit.components.v1 as components

from Optimiser.main import optimisation
# from Transfer import *
# from CRS.Transfer import *
from CRS.crs_init import CRSConvertor

# Page configuration
st.set_page_config(
    page_title="Wind Farm Layout Optimisation",
    layout="wide"
)
st.markdown('# Wind Farm Layout Optimisation')

# Default map position (Whitelee Wind Farm)
default = {
    'centre': [55.674099775230026, -4.271278381347657],
    'zoom': 12,
    'site': [[55.634359319706036, -4.364543821199962], [55.714704134580245, -4.183104393719847]]
}


# 55.714704134580245,
# -4.364543821199962,
# 55.634359319706036,
# -4.183104393719847


def initialise_session_state():
    """
    This function is to initialise st.session_state based on default settings.
    :return:
    """
    # Initialise session state for wind turbine locations
    if 'wt_pos' not in st.session_state:
        st.session_state['wt_pos'] = []
    # Initialise the wind farm site boundaries
    if 'site' not in st.session_state:
        st.session_state['site'] = default['site']
    # Initialise map position
    if 'centre' not in st.session_state:
        st.session_state['centre'] = default['centre']
    if 'zoom' not in st.session_state:
        st.session_state['zoom'] = default['zoom']


def reset_session_state():
    """
    This function is to force resetting st.session_state.
    :return:
    """
    # Reset session state for wind turbine locations
    st.session_state['wt_pos'] = []
    # Reset the wind farm site boundaries
    st.session_state['site'] = default['site']
    # Reset the map range
    st.session_state['centre'] = default['centre']
    st.session_state['zoom'] = default['zoom']


def initialise_map(centre, zoom):
    _m = folium.Map(location=centre, zoom_start=zoom)
    return _m


# Initialisation
initialise_session_state()
m = initialise_map(st.session_state['centre'], st.session_state['zoom'])
MousePosition().add_to(m)

# Enable export without the edit parameter
# Draw(export=True).add_to(m)

# Add a form for input
with st.form('config'):
    st.markdown('### Optimisation Configurations')
    st.selectbox('Wind farm site:', ('Whitelee Wind Farm'), key='case')
    st.number_input('Wind turbine number:', min_value=1, step=1, key='wt_number')
    submit = st.form_submit_button('Submit')

# on clicking the submit button
if submit:
    reset_session_state()
    m = initialise_map(st.session_state['centre'], st.session_state['zoom'])

    site = st.session_state['site']
    conv = CRSConvertor([site[1][0], site[0][1], site[0][0], site[1][1]])
    solution = optimisation(st.session_state['wt_number'])
    solution = conv.gene_to_pos(solution)
    st.session_state['wt_pos'] = solution

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

if st.button('Clear All'):
    reset_session_state()
    m = initialise_map(st.session_state['centre'], st.session_state['zoom'])

fg = folium.FeatureGroup(name='Wind_Turbines')
for pos in st.session_state['wt_pos']:
    fg.add_child(folium.Marker(pos))
fg.add_child(folium.Rectangle(st.session_state['site']))


# Show map
st_folium(m, feature_group_to_add=fg, width=900, height=500, key="map1")
# Show data
# st.write(st.session_state)
