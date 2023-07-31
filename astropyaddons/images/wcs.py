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
        wcs = astropy.wcs.WCS(header.header)

        # First, detect if the image is NOT plate-solved.
        if all(wcs.pixel_to_world_values(([0,1], [0,1]))[0] == np.array([1,2])):
            # If it is not, we will set our WCS information to "None"
            self.wcs = None
            self.coords = None
            return
        

        # Otherwise, create a "coordinate grid" that can be indexed via self.coords[(x, y)]
        self.wcs = wcs
        
        # Create an array of coordinates [(0, 0), (0, 1), (0, 2), ..., (1, 0), (1, 1), ...]
        coordinates = \
            np.array(np.meshgrid(
                np.arange(0, header.size_y), np.arange(0, header.size_x)
            )).T.reshape(-1, 2)
        wcs_coords = self.wcs.pixel_to_world_values(coordinates)

        # Reshape into an array indexed with `self.coords[y, x]`
        self.coords = np.transpose(
            np.array(wcs_coords).reshape(header.size_y, header.size_x, 2),
            (1,0,2)
        )
        


