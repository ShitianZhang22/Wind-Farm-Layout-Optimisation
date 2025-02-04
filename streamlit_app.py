import streamlit as st
import folium
from folium.plugins import MousePosition, Draw
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import numpy as np

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
    # Reset data
    st.session_state['site_summary'] = []
    st.session_state['wt_summary'] = None


# Initialisation
initialise_session_state()
m = folium.Map(location=st.session_state['centre'], zoom_start=st.session_state['zoom'])
MousePosition().add_to(m)

# Enable export without the edit parameter
draw = Draw(draw_options={
    'polyline': False,
    'polygon': False,
    'rectangle': {},
    'circle': False,
    'marker': False,
    'circlemarker': False,
    })
draw.add_to(m)

# The first section of Optimisation Request Form
st.markdown('## Optimisation Request Form')
# Add a form for input
with st.form('config'):
    st.selectbox('Wind farm site', ('Whitelee Wind Farm', 'User defined area in the map'), key='case')
    st.number_input('Wind turbine number', min_value=1, value=215, step=1, key='wt_number')
    submit = st.form_submit_button('Submit')

# on clicking the submit button
if submit:

    # option of customised site
    if st.session_state['case'] == 'User defined area in the map':
        if st.session_state['map1']['last_active_drawing'] is not None:
            shape = st.session_state['map1']['last_active_drawing']['geometry']['coordinates'][0]
            st.session_state['site'] = [[shape[0][1], shape[0][0]], [shape[2][1], shape[2][0]]]
            site = st.session_state['site']
            st.session_state['centre'] = [(site[0][0] + site[1][0]) / 2, (site[0][1] + site[1][1]) / 2]
            st.session_state['zoom'] = np.floor(np.log2(360 * 500 / 256 / (site[1][0] - site[0][0]))) - 1
    # option of case study        
    else:
        st.session_state['site'] = default['site']
        st.session_state['centre'] = default['centre']
        st.session_state['zoom'] = default['zoom']


    reset_session_state()
    m = folium.Map(location=st.session_state['centre'], zoom_start=st.session_state['zoom'])

    site = st.session_state['site']

    # if the site is the same with the previous one, we don't need to get the wind data and land data again.
    if site == st.session_state['history']['site']:
        conv = st.session_state['history']['conv']
        wind_data = st.session_state['history']['wind']
        feasible_cell = st.session_state['history']['feasible_cell']
    else:
        conv = CRSConvertor([site[1][0], site[0][1], site[0][0], site[1][1]])
        wind_data = wind([site[1][0], site[0][1], site[0][0], site[1][1]], 'Wind/data/summary-1d.nc')
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


# st.markdown('##')
fg = folium.FeatureGroup(name='Wind_Turbines')
for pos in st.session_state['wt_pos']:
    fg.add_child(folium.Marker(pos))
fg.add_child(folium.Rectangle(st.session_state['site']))

# Show map
st_folium(m, feature_group_to_add=fg, height=500, key="map1", use_container_width=True)

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
