from .header import Header

import astropy.wcs
import numpy as np

class WCS:
    """
    World coordinate system (WCS) obtained from a FITSImage. 
    Extracts the WCS information and neatly keeps it in a class.

    Parameters:
     - `header`: `astropy.io.fits.header.Header` object to create
        a WCS from.
    """

    def __init__(self, header: Header):

        # Initialize WCS object
        wcs = astropy.wcs.WCS(Header.header)

        # First, detect if the image is plate-solved.
        if any(wcs.pixel_to_world_values(([0,1], [0,1]))[0] == np.array([1,2])):
            # If it is not, we will set our WCS information to "None"
            self.wcs = None
            self.coords = None
            return
        

        # Otherwise, create a "coordinate grid" that can be indexed via self.coords[(x, y)]
        self.wcs = wcs
        
        coordinate_pairs = \
            np.array(np.meshgrid(
                np.arange(0, header.size_x), np.arange(0, header.size_y)
            )).T.reshape(-1, 2)
        wcs_pairs = self.wcs.pixel_to_world_values(coordinate_pairs)

        # Reshape into a (size_x, size_y) array
        self.coords = np.array(wcs_pairs).reshape(header.size_x, header.size_y, 2)
        


