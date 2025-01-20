"""
This file is for converting the hourly wind data to the annual wind distribution.
Input: an (time, 2) ndarray of the u and v component of the hourly wind speed
Return: an (8, ) ndarray of the average wind speed at 8 directions
"""

import numpy as np


def accumulate(uv):
    """
    This function is for converting the hourly wind data to the annual wind distribution.
    `uv`: an (time, 2) ndarray of the u and v component of the hourly wind speed in uv form
    Return: an (8, ) ndarray of the average wind speed and frequency at 8 directions
    """
    # print(uv)
    # the original wind speed data is eastward and northward, which should be revesed
    uv = -uv
    wind = np.zeros(uv.shape, dtype='float64')
    wind[:, 0] = (uv[:, 0] ** 2 + uv[:, 1] ** 2) ** 0.5
    wind[:, 1] = np.arcsin(uv[:, 0] / wind[:, 0])
    mask = uv[:, 1] < 0
    wind[mask, 1] = np.pi - wind[mask, 1]

    # categorising the wind into 8 directions
    wind[:, 1] = (wind[:, 1] + np.pi / 8) * 4 // np.pi
    # print(wind)

    # summarise
    summary = np.zeros((8, 2), dtype='float64')
    for i in range(8):
        mask = wind[:, 1] == i
        summary[i, 1] = mask.sum()
        if summary[i, 1]:
            summary[i, 0] = wind[mask, 0].mean()
    summary[:, 1] /= summary[:, 1].sum()
    return summary


if __name__ == '__main__':
    data = np.loadtxt('raw/test_uv.txt', encoding='utf-8')
    print(accumulate(data))
