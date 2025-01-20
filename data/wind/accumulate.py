"""
This file is for converting the hourly wind data to the annual wind distribution.
Input: an (time, 2) ndarray of the u and v component of the hourly wind speed
Return: an (8, ) ndarray of the average wind speed at 8 directions
"""

import numpy as np


def accumulate(wind):
    """
    This function is for converting the hourly wind data to the annual wind distribution.
    `wind`: an (time, 2) ndarray of the u and v component of the hourly wind speed
    Return: an (8, ) ndarray of the average wind speed at 8 directions
    """
    print(wind)

if __name__ == '__main__':
    data = np.loadtxt('raw/test_uv.txt', encoding='utf-8')
    accumulate(data)
