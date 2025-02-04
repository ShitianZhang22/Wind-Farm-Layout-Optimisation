"""
This is the master structure managing the process of wind data, including:
1. Downloading and deleting the temporary file of wind data
2. Get the data from the raw data downloaded
3. Converting the data to annual wind distribution

Input: a list of site bounds, and a path for caching data.
Return: an (8, 2) ndarray of the average wind speed and frequency at 8 directions
"""

from Aborted.Wind.get_wind import get_wind
from Aborted.Wind.process_wind import process_wind
from Aborted.Wind.accumulate import accumulate
from Aborted.Wind.local_summary import local_sum
import os
import numpy as np


def wind(area, save_dir, years, months, test=False, local=True):
    """
    This is the master structure managing the process of wind data.

    `area`: a list of Northern, Western, Southern, Eastern bounds of the site.
    `save_dir`: the directory to temporarily save the downloaded data.
    `years`: a list of strings including the years
    `months`: a list of strings including the months
    `*test`: a bool for triggering test mode, where the data downloading process is skipped.
    `*local`: a bool for triggering local mode, where local post-processed data is used.
    Return: an (8, 2) ndarray of the average wind speed and frequency at 8 directions
    """
    # get the centre of the site
    lat, lon = (area[0] + area[2]) / 2, (area[1] + area[3]) / 2
    if local:
        return local_sum(save_dir, lat, lon)
    else:
        if test: 
            raw_wind = process_wind('Wind/backup/temp.nc', lat, lon)
        else:
            raw_wind = np.zeros((0, 2), dtype='float64')
            for i in range(len(years)):
                for j in range(len(months)):
                    get_wind(area, save_dir, years[i], months[j])
                    raw_wind = np.concatenate((raw_wind, process_wind(save_dir, lat, lon)), axis=0)
                    os.remove(save_dir)
        return accumulate(raw_wind)

if __name__ == '__main__':
    test_area = [55.7146943, -4.364574, 55.6343709, -4.1830774]
    dir = 'raw/temp.nc'
    y = ['2024']
    m = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    print(wind(test_area, dir, y, m, True))

