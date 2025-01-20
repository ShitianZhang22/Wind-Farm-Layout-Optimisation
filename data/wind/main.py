"""
This is the master structure managing the process of wind data, including:
1. Downloading and deleting the temporary file of wind data
2. Get the data from the raw data downloaded
3. Converting the data to annual wind distribution
"""

from get_wind import get_wind
from process_wind import process_wind
from accumulate import accumulate

