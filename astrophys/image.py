from .fitsimage import FITSImage
from .star import Star

class Image:
    """
    Overarching class to group `FITSImage` objects and `Star` objects
    """
    def __init__(self, fits_image: FITSImage, stars: list[Star]):
        """
        Overarching class to group `FITSImage` objects and `Star` objects

        Parameters:
          - `fits_image`: `FITSImage` object
          - `stars`: list of `Star` objects
        """
        self.fits_image = fits_image
        self.stars = stars

    def __repr__(self) -> str:
        return f'Image consisting of FITS Image [{self.fits_image.filter}, {self.fits_image.date}, {self.fits_image.time}] '\
          f'and {self.stars.__len__()} stars, {[star.label for star in self.stars]}' 