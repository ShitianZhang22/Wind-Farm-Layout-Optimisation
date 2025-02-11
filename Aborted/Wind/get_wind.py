"""
This file is for downloading wind data from ERA5-land.
Input: a list of site bounds, and a path for caching data.
Return: No return
The downloaded data will be stored in Wind/raw/temp.nc
"""

import cdsapi


def get_wind(area, save_dir, year, month):
    """
    This file is for downloading wind data from ERA5-land.
    `area`: a list of Northern, Western, Southern, Eastern bounds of the site.
    `save_dir`: a string of the directory to temporarily save the downloaded data.
    `year`: a string or integer of the year (only one at a time)
    `month`: a string or integer of the month (only one at a time)
    Return: No return
    The downloaded data will be stored in Wind/raw/temp.nc
    """
    print('Requesting data in {}'.format((year, month)))
    year = str(year)
    month = str(month)

    dataset = "reanalysis-era5-land"
    all_day = ["01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"]
    day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    request = {
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind"
        ],
        "year": "2024",
        "month": month,
        "day": all_day[:day_in_month[int(month) - 1]],
        "time": [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": area
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request, save_dir)


if __name__ == '__main__':
    test_area = [55.714704134580245, -4.364543821199962, 55.634359319706036, -4.183104393719847]
    dir = 'raw/temp.nc'
    get_wind(test_area, dir, '2024', '12')
