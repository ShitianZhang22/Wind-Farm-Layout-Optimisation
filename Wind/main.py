"""
This is the master structure managing the process of wind data, including:
1. Downloading and deleting the temporary file of wind data
2. Get the data from the raw data downloaded
3. Converting the data to annual wind distribution

Input: a list of site bounds, and a path for caching data.
Return: an (8, ) ndarray of the average wind speed at 8 directions
"""

from Wind.get_wind import get_wind
from Wind.process_wind import process_wind
from Wind.accumulate import accumulate
import os


def wind(area, save_dir, test=False):
    """
    This is the master structure managing the process of wind data.

    `area`: a list of Northern, Western, Southern, Eastern bounds of the site.
    `save_dir`: the directory to temporarily save the downloaded data.
    `*test`: a bool for triggering test mode, where the data downloading process is skipped.
    Return: an (8, ) ndarray of the average wind speed at 8 directions
    """
    # get the centre of the site
    lat, lon = (area[0] + area[2]) / 2, (area[1] + area[3]) / 2
    if test: 
        raw_wind = process_wind('Wind/backup/temp.nc', lat, lon)
    else:
        get_wind(area, save_dir)
        raw_wind = process_wind(save_dir, lat, lon)
        os.remove(save_dir)
    return accumulate(raw_wind)

if __name__ == '__main__':
    test_area = [55.7146943, -4.364574, 55.6343709, -4.1830774]
    dir = 'raw/temp.nc'
    print(wind(test_area, dir, True))

