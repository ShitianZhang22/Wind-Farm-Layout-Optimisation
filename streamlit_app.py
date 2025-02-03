import streamlit as st
import folium
from folium.plugins import MousePosition
from streamlit_folium import st_folium
import streamlit.components.v1 as components

from Optimiser.main import optimisation
from CRS.crs_init import CRSConvertor
from Wind.main import wind
from Land.main import land

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
    # history
    if 'history' not in st.session_state:
        st.session_state['history'] = {
        'site': None,
        'conv': None,
        'wind': None,
        'feasible_cell': None,
    }
    # Initialise map position
    if 'centre' not in st.session_state:
        st.session_state['centre'] = default['centre']
    if 'zoom' not in st.session_state:
        st.session_state['zoom'] = default['zoom']
    if 'site_summary' not in st.session_state:
        st.session_state['site_summary'] = []
    if 'wt_summary' not in st.session_state:
        st.session_state['wt_summary'] = None


def reset_session_state():
    """
    This function is to force resetting st.session_state.
    :return:
    """
    # Reset session state for wind turbine locations
    st.session_state['wt_pos'] = []
    # Reset the map range
    st.session_state['centre'] = default['centre']
    st.session_state['zoom'] = default['zoom']
    # Reset data
    st.session_state['site_summary'] = []
    st.session_state['wt_summary'] = None


def initialise_map(centre, zoom):
    _m = folium.Map(location=centre, zoom_start=zoom)
    return _m


# Initialisation
initialise_session_state()
m = initialise_map(st.session_state['centre'], st.session_state['zoom'])
MousePosition().add_to(m)

# Enable export without the edit parameter
# Draw(export=True).add_to(m)

# The first section of Optimisation Request Form
st.markdown('## Optimisation Request Form')
# Add a form for input
with st.form('config'):
    st.selectbox('Wind farm site:', ('Whitelee Wind Farm'), key='case')
    st.number_input('Wind turbine number:', min_value=1, step=1, key='wt_number')
    submit = st.form_submit_button('Submit')

# on clicking the submit button
if submit:
    reset_session_state()
    m = initialise_map(st.session_state['centre'], st.session_state['zoom'])

    site = st.session_state['site']

    # if the site is the same with the previous one, we don't need to get the wind data and land data again.
    if site == st.session_state['history']['site']:
        conv = st.session_state['history']['conv']
        wind_data = st.session_state['history']['wind']
        feasible_cell = st.session_state['history']['feasible_cell']
    else:
        conv = CRSConvertor([site[1][0], site[0][1], site[0][0], site[1][1]])
        wind_data = wind([site[1][0], site[0][1], site[0][0], site[1][1]], 'Wind/backup/summary-1d.nc', ['2024'], ['12'], True, True)
        feasible_cell = land('Land/data/infeasible.nc', conv.grid_gcs)
    solution, summary, efficiency, st.session_state['wt_summary'] = optimisation(st.session_state['wt_number'], conv.rows, conv.cols, wind_data, feasible_cell)
    solution = conv.gene_to_pos(solution)
    st.session_state['site_summary'] = [summary, efficiency]
    st.session_state['wt_pos'] = solution

    # save history
    st.session_state['history'] = {
        'site': st.session_state['site'].copy(),
        'conv': conv,
        'wind': wind_data.copy(),
        'feasible_cell': feasible_cell.copy(),
    }

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

# st.markdown('##')
fg = folium.FeatureGroup(name='Wind_Turbines')
for pos in st.session_state['wt_pos']:
    fg.add_child(folium.Marker(pos))
fg.add_child(folium.Rectangle(st.session_state['site']))

# Show map
st_folium(m, feature_group_to_add=fg, width=1000, height=500, key="map1")
# if st.button('Clear All'):
#     reset_session_state()
#     m = initialise_map(st.session_state['centre'], st.session_state['zoom'])

# The last part of summary
st.markdown('## Summary')

col1, col2 = st.columns(2)
with col1:
    if len(st.session_state['site_summary']) != 0:
        st.markdown('- ### Data of wind farm site')
        st.markdown('The estimated Annual Energy Production is')
        st.markdown('## {:.2f} MWh'.format(st.session_state['site_summary'][0]))
        st.markdown('with the overall efficiency of')
        st.markdown('### {:.2%}'.format(st.session_state['site_summary'][1]))
    else:
        st.markdown('Please run optimisation first!')

with col2:
    if len(st.session_state['site_summary']) != 0:
        st.markdown('- ### Data of wind turbines')
        st.dataframe(
            st.session_state['wt_summary'],
            hide_index=True,
            column_config={
                'Annual Energy Production': st.column_config.NumberColumn(format='%.2f kWh'),
                'Efficiency': st.column_config.NumberColumn(format='%.2f %%'),
            },
            )
# Show data
# st.write(st.session_state)
