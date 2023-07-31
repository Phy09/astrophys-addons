from astropy.io import fits
import matplotlib.pyplot as plt

from ..grid import Grid
from .header import Header
from .wcs import WCS

class FITSImage:
    """
    Class to handle FITS images. Load with `FITSImage(filepath)`.
    """

    def __init__(self, filepath, id: int=None):
        """
        Parameters:
         - `filepath`: filepath of FITS image to load.
         - `id`: which image to load of the file (index).
            If none specified, will load the first image.
        """

        # LOAD FITS FILE
        with fits.open(filepath) as images:
            if id is None:
                id = 0
                if len(images) != 1:
                    print(f"No image id specified for FITS image {filepath}."\
                        "Only the first one will be loaded.")
            
            # Extract useful information from the fits image.
            self.header: Header = Header(images[id].header)
            self.grid: Grid = Grid(images[id].data)

        # Establish the WCS.
        self.wcs: WCS = WCS(self.header)

    def __repr__(self):
        return f'FITSImage of [{self.header.filter}, {self.header.datetime}, exptime {self.header.exptime}s]'
    
    def quickplot(self, phi_lo: float=-1, phi_hi: float=3) -> None:
        """
        Displays a simple grayscale plot of the data. 
        
        Parameters:
          - `lo_phi`: standard deviations from median to assign to black
          - `hi_phi`: standard deviations from median to assign to white
        """
        assert phi_lo < phi_hi, "lo_phi must be lower than hi_phi"

        lo = self.grid.median + phi_lo*self.grid.std
        hi = self.grid.median + phi_hi*self.grid.std

        plt.figure(figsize=(10,10))
        plt.title(self.__repr__())
        plt.imshow(self.grid.grid, cmap='gray', origin='lower', vmin=lo, vmax=hi)