from astropy.io import fits

from ..grid import Grid
from .header import Header
from .wcs import WCS

class FITSImage:
    """
    Class to handle FITS images. Load with `FITSImage(filepath)`.
    """

    def __init__(self, filepath, image_to_load: int=None):
        """
        Parameters:
         - `filepath`: filepath of FITS image to load.
         - `image_to_load`: which image to load of the file.
            If none specified, will load the first image.
        """

        # LOAD FITS FILE
        with fits.open(filepath) as fits_image:
            if image_to_load is None:
                image_to_load = 0
                if len(fits_image) != 1:
                    print(f"Warning: FITS image with filepath {self.fp}"\
                            "has multiple images."\
                            "Only the first one will be loaded.")
            
            # Extract useful information from the fits image.
            self.header: Header = Header(fits_image[image_to_load].header)
            self.grid: Grid = Grid(fits_image[image_to_load].data)

        # Establish the WCS.
        self.wcs: WCS = WCS(self.header)

    def __repr__(self):
        return f'FITSImage of [{self.filter}, {self.date}, {self.time}, exptime {self.exptime}s]'