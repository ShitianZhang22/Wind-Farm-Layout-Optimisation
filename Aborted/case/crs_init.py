"""
This file is for finding the appropriate CRS for the wind farm site, providing a method for conversion.
"""

from pyproj import CRS, Transformer
from pyproj.database import query_utm_crs_info
from pyproj.aoi import AreaOfInterest
import numpy as np

class CRSConvertor:
    """
    This is a class for converting the CRS. Upon instantiation, a CRS will be found for the wind farm site.
    Besides, the geographical coordinates of all cell centres will be calculated in advance.
    `bounds`: a list of site range (geographical coordinate of Northern, Western, Southern, Eastern bounds (by order))
    """
    def __init__(self, bounds):
        aoi = AreaOfInterest(bounds[1], bounds[2], bounds[3], bounds[0])
        utm_crs_list = query_utm_crs_info(datum_name='WGS 84', area_of_interest=aoi)
        gcs = "EPSG:4326"  # WGS 84 (Geographic Coordinate System)
        if utm_crs_list:
            # Use the first (and most likely only) result as the projected coordinate system
            pcs = CRS.from_epsg(utm_crs_list[0].code)
            self.transformer = Transformer.from_crs(gcs, pcs, always_xy=True)
            # print('{} is used for the wind farm site.'.format(pcs))

            # Set the Southwestern corner of the site as the origin, 
            # and cut the northern and eastern edge of the site to fit the cell size
            corner1 = list(self.to_pcs(bounds[2], bounds[1]))
            corner2 = list(self.to_pcs(bounds[0], bounds[3]))

            # calculate the number of rows and columns
            cell_size = 154
            self.rows = int((corner2[0] - corner1[0]) // cell_size)
            self.cols = int((corner2[1] - corner1[1]) // cell_size)

            # get all the grid centres and the corresponding PCS
            grid_pcs = np.zeros((self.rows, self.cols, 2), dtype='float64')
            temp = corner1[0] + cell_size / 2
            for i in range(self.rows):
                grid_pcs[i, :, 0] = temp
                temp += cell_size
            temp = corner1[1] + cell_size / 2
            for i in range(self.cols):
                grid_pcs[:, i, 1] = temp
                temp += cell_size
            
            # Then convert the coordinates to GCS and flatten the grid
            self.grid_gcs = np.zeros((self.rows, self.cols, 2), dtype='float64')
            for i in range(self.rows):
                for j in range(self.cols):
                    self.grid_gcs[i, j, 0], self.grid_gcs[i, j, 1] = self.to_gcs(grid_pcs[i, j, 0], grid_pcs[i, j, 1])
            self.grid_gcs = self.grid_gcs.reshape(self.rows * self.cols, 2)
        else:
            raise ValueError("No UTM CRS found for the given location.")

    def to_pcs(self, _lat, _lon):
        """
        This function is for converting the geographical coordinate to projected coordinate.
        `_lat`: a float of latitude.
        `_lon`: a float of longitude.
        return: a tuple of converted coordinates (lat, lon).
        """
        result = self.transformer.transform(_lon, _lat)
        return result[1], result[0]

    def to_gcs(self, _lat, _lon):
        """
        This function is for converting the projected coordinate to geographical coordinate.
        `_lat`: a float of latitude.
        `_lon`: a float of longitude.
        return: a tuple of converted coordinates.
        """
        result = self.transformer.transform(_lon, _lat, direction='INVERSE')
        # print(result)
        return result[1], result[0]
    
    def gene_to_pos(self, _gene):
        """
        This function is used in Streamlit_app.py to transform the optimisation result to GCS for visualisation.
        `_gene`: a list including the one dimensional indices of optimised wind turbines.
        return: a (n, 2) list of the GCS of wind turbines.
        """
        return self.grid_gcs[_gene].tolist()

    

if __name__ == '__main__':
    conv = CRSConvertor([55.714704134580245, -4.364543821199962, 55.634359319706036, -4.183104393719847])
    # conv.to_pcs(55.7146943, -4.364574)
    conv.to_gcs(6175170.125734458, 414271.5627967309)
    print(conv.grid_gcs)
