"""
This file is for finding the appropriate CRS for the wind farm site, providing a method for conversion.
"""

from pyproj import CRS, Transformer
from pyproj.database import query_utm_crs_info
from pyproj.aoi import AreaOfInterest

class CRSConvertor:
    """
    This is a class for converting the CRS. Upon instantiation, a CRS will be found for the wind farm site.
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
            print('{} is used for the wind farm site.'.format(pcs))
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

if __name__ == '__main__':
    conv = CRSConvertor([55.7146943, -4.364574, 55.6343709, -4.1830774])
    # conv.to_pcs(55.7146943, -4.364574)
    conv.to_gcs(6175170.125734458, 414271.5627967309)

    