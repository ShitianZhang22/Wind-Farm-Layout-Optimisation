import folium.features
import folium.raster_layers
import streamlit as st
import folium
from folium.plugins import MousePosition, Draw
from branca.element import Template, MacroElement
from streamlit_folium import st_folium
import numpy as np

from Optimiser.main import optimisation
from Optimiser.config_ss import cell_width
from CRS.crs_init import CRSConvertor
from Wind.main import wind
from Land.main import land, feasibility

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
    if 'optimised' not in st.session_state:
        st.session_state['optimised'] = False


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
# This function is temporarily aborted
# draw.add_to(m)

# The first section of Optimisation Request Form
st.markdown('## Optimisation Request Form')
# Add a form for input
with st.form('config'):
    # The function of customise area is temporarily aborted
    # st.selectbox('Wind farm site', ('Whitelee Wind Farm', 'User defined area in the map'), key='case')
    st.selectbox('Wind farm site', ('Whitelee Wind Farm',), key='case')
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
    # m = folium.Map(location=st.session_state['centre'], zoom_start=st.session_state['zoom'])

    site = st.session_state['site']

    # if the site is the same with the previous one, we don't need to get the wind data and land data again.
    if site == st.session_state['history']['site']:
        conv = st.session_state['history']['conv']
        wind_data = st.session_state['history']['wind']
        feasible_cell = st.session_state['history']['feasible_cell']
    else:
        conv = CRSConvertor([site[1][0], site[0][1], site[0][0], site[1][1]], cell_width)
        wind_data = wind([site[1][0], site[0][1], site[0][0], site[1][1]], 'Wind/data/summary-01d.nc')
        if st.session_state['case'] == 'Whitelee Wind Farm':  # this is for storing the infeasible area for Whitelee Wind Farm
            feasible_cell = land('Land/data/infeasible.nc', conv.grid_gcs, st.session_state['case'])
            # feasible_cell = land('Land/data/infeasible.nc', conv.grid_gcs)
        else:
            feasible_cell = land('Land/data/infeasible.nc', conv.grid_gcs)
    solution, summary, efficiency, st.session_state['wt_summary'] = optimisation(st.session_state['wt_number'], conv.rows, conv.cols, wind_data, feasible_cell)
    solution = conv.gene_to_pos(solution)
    st.session_state['site_summary'] = [summary, efficiency]
    st.session_state['wt_pos'] = solution
    
    st.session_state['optimised'] = True

    # save history
    st.session_state['history'] = {
        'site': st.session_state['site'].copy(),
        'conv': conv,
        'wind': wind_data.copy(),
        'feasible_cell': feasible_cell.copy(),
    }


fg = folium.FeatureGroup(name='Wind_Turbines')
 
# add wind turbine icon
for i in range(len(st.session_state['wt_pos'])):
    temp = st.session_state['wt_pos'][i]
    # EACH ICON CAN ONLY BE USED ONCE!!!!!
    icon = folium.features.CustomIcon(
    'icon/turbine.png',
    icon_size=(50, 50),
    icon_anchor=(24, 42),
    )
    tooltip = 'Annual Energy Production: {:,.2f} MWh <br> Efficiency: {:.2%}'.format(st.session_state['wt_summary'][i, 0], st.session_state['wt_summary'][i, 1])
    fg.add_child(folium.Marker(location=temp, icon = icon, tooltip=tooltip))
fg.add_child(folium.Rectangle(st.session_state['site']))

# add feasibility layer
st.markdown('*Hover over a turbine to view energy production.*')
site = st.session_state['site']
rgba_img, f_bounds = feasibility('Land/data/infeasible.nc', [site[1][0], site[0][1], site[0][0], site[1][1]])

folium.raster_layers.ImageOverlay(
    image=rgba_img,
    bounds=f_bounds,
    origin='lower',
    opacity=1,
).add_to(m)

if st.session_state['optimised']:
    pass
else:
    st.markdown('**Click Submit button to start optimisation!**')


# Create the legend template as an HTML element
# Source: https://stackoverflow.com/questions/77931522/how-to-add-a-legend-to-streamlit-folium-map-when-there-is-few-discrete-colors
legend_template = """
{% macro html(this, kwargs) %}
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.7);
     border-radius: 6px; padding: 10px; font-size: 14px; font-weight: bold; right: 20px; top: 300px;'>   
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li style='font-size: 20px; padding: 10px;'>Legend</li>
    <li><img src="https://github.com/ShitianZhang22/Wind-Farm-Layout-Optimisation/blob/main/icon/boundary.png?raw=true" style="width: 30px; height: 30px; margin-right: 5px;">Site Boundary</li>
    <li><img src="https://github.com/ShitianZhang22/Wind-Farm-Layout-Optimisation/blob/main/icon/infeasible.png?raw=true" style="width: 30px; height: 30px; margin-right: 5px;">Infeasible Area</li>
    <li><img src="https://github.com/ShitianZhang22/Wind-Farm-Layout-Optimisation/blob/main/icon/turbine-small.png?raw=true" style="width: 30px; height: 30px; margin-right: 5px;">Wind Turbine</li>
  </ul>
</div>
</div> 
<style type='text/css'>
  .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
  .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
  .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
</style>
{% endmacro %}
"""
# Add the legend to the map
macro = MacroElement()
macro._template = Template(legend_template)
m.get_root().add_child(macro)

# Show map
st_folium(m, feature_group_to_add=fg, height=500, key="map1", use_container_width=True, pixelated=True)


# The last part of summary
st.markdown('## Summary')

col1, col2, col3 = st.columns(3)
with col1:
    if len(st.session_state['site_summary']) != 0:
        st.markdown('The estimated Annual Energy Production is')
        st.markdown('### {:,.2f} MWh'.format(st.session_state['site_summary'][0]))
    else:
        st.markdown('Please run optimisation first!')

with col2:
    if len(st.session_state['site_summary']) != 0:
        st.markdown('Equivalent to')
        st.markdown('### {:,.0f} household consumption*'.format(st.session_state['site_summary'][0] // 2.7))
        st.markdown('*Typical annual household electricity use estimated by Ofgem.')

with col3:
    if len(st.session_state['site_summary']) != 0:
        st.markdown('The overall efficiency is')
        st.markdown('### {:.2%}'.format(st.session_state['site_summary'][1]))

# Show data
# st.write(st.session_state)
