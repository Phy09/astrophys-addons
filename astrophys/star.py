import numpy as np

from .fitsimage import FITSImage
from .region import Region, CircleRegion, AnnulusRegion, SubAnnulusRegion

class Star:
    """
    Class to define a star in an image.
    """
    def __init__(self, fits_image: FITSImage, center, aperture_size: float, annulus_r1: float, annulus_r2: float, label: str=None):
        """
        Class to define a star given an image and parameters.

        Parameters:
          - `fits_image`: `FITSImage` object that the star is in.
          - `center`: `(y, x)` coordinates of the star in the image.
          - `aperture_size`: size of aperture for flux sampling.
          - `annulus_r1`: inner radius of annulus for background sampling.
          - `annulus_r2`: outer radius of annulus for background sampling.
          - `label`: (optional) label for the star
        """
        self.fits_image = fits_image
        self.center = center
        self.aperture_size = aperture_size
        self.annulus_r1 = annulus_r1
        self.annulus_r2 = annulus_r2

        self.aperture = CircleRegion(fits_image, center, aperture_size)
        self.annulus = AnnulusRegion(fits_image, center, annulus_r1, annulus_r2)

        self.label = label

        # Magnitudes
        self._magnitude = None
        self._k = None
        self._magnitude_err = None
        self._k_err = None

        # Evaluate errors associated with aperture and annulus
        self.evaluate_aperture_errors()
        self.evaluate_annulus_errors()

    @property
    def flux(self):
        return self.aperture.sum - self.annulus.median * self.aperture.n
    @property
    def flux_err(self):
        return np.abs(self.annulus.median_err*self.aperture.n)

    @property
    def magnitude(self):
        if self._magnitude is not None:
            return self._magnitude
        if self._k is None:
            raise ValueError("The calibration constant `k` is not yet defined.")
        
        self._magnitude = -2.5*np.log10(self.flux) + self._k
        return self._magnitude
    @property
    def k(self):
        if self._k is not None:
            return self._k
        if self._magnitude is None:
            raise ValueError("The magnitude of the star is not yet defined.")
        
        self._k = 2.5*np.log10(self.flux) + self._magnitude
        return self._k
    
    @property
    def magnitude_err(self):
        if self._magnitude_err is not None:
            return self._magnitude_err
        if self._k_err is None:
            raise ValueError("The ERROR in the calibration constant `k` is not yet defined")
        
        self._magnitude_err = ((self._k_err**2) + (self.flux_err/self.flux)**2) ** 0.5
        return self._magnitude_err
    @property
    def k_err(self):
        if self._k_err is not None:
            return self._k_err
        if self._magnitude_err is None:
            raise ValueError("The ERROR in the magnitude of the star is not yet defined")
        
        self._k_err = ((self._magnitude_err**2) + (self.flux_err/self.flux)**2) ** 0.5
        return self._k_err
        

    def evaluate_aperture_errors(self) -> None:
        """
        Evaluate the errors associated with centring and size of the aperture region.
        """
        aperture_medians = []
        aperture_means = []

        # Resolution to run region error calculation
        RESOLUTION = 5
        # The line below creates np.arrays for the offsets in center positions
        # array([-0.5, -0.5], [-0.5, -0.25], ...)
        center_offsets = np.array(np.meshgrid(np.linspace(-0.5, 0.5, RESOLUTION), np.linspace(-0.5, 0.5, RESOLUTION))).T.reshape(-1,2)

        for size_offset, center_offset in center_offsets:
            aperture = CircleRegion(self.fits_image, self.center + center_offset, self.aperture_size + size_offset)
            
            aperture_medians.append(aperture.median)
            aperture_means.append(aperture.mean)

        self.aperture.median_err = np.std(aperture_medians) / RESOLUTION
        self.aperture.mean_err = np.std(aperture_means) / RESOLUTION

    def evaluate_annulus_errors(self) -> None:
        """
        Evaluate the errors associated with the annulus
        """
        self.subannulus_regions = []

        subannulus_medians = []
        subannulus_means = []

        # Resolution to run annulus error calculation
        RESOLUTION = 8

        angles = np.linspace(0, 360, RESOLUTION+1)

        for i in range(RESOLUTION):
            angle_min, angle_max = angles[i], angles[i+1]
            sub_region = SubAnnulusRegion(self.fits_image, self.center, self.annulus_r1, self.annulus_r2, angle_min, angle_max)

            self.subannulus_regions.append(sub_region)
            subannulus_medians.append(sub_region.median)
            subannulus_means.append(sub_region.mean)
        
        self.annulus.median_err = np.std(subannulus_medians) / np.sqrt(RESOLUTION)
        self.annulus.mean_err = np.std(subannulus_means) / np.sqrt(RESOLUTION)

    @property
    def statistics(self):
        return \
            f'Star: {self.label if self.label is not None else "-"}\n'\
            f'----------------\n'\
            f'Aperture Statistics:\n'\
            f'npix: {self.aperture.n}\n'\
            f'sum: {self.aperture.sum}\n'\
            f'\n'\
            f'Annulus Statistics:\n'\
            f'npix: {self.annulus.n}\n'\
            f'fmedian background: {self.annulus.median}\n'\
            f'\n'\
            f'Flux: {self.flux} +- {self.flux_err}\n'

    def __repr__(self):
        return f'Star: {self.label} of {self.fits_image}'