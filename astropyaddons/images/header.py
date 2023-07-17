from astropy.io import fits

class Header:
    """
    Header obtained from FITSImage. Extracts useful information
    and keeps it tidy in its own class.

    Parameters:
     - `header`: `astropy.io.fits.header.Header` object
    """
    def __init__(self, header: fits.header.Header):
        self.header = header
        
        ### Extracting useful values.

        # GENERAL OBSERVATION DETAILS
        self.exptime        = self.header.get('EXPTIME' , default=None)
        self.datetime       = self.header.get('DATE-OBS', default=None)
        self.JD             = self.header.get('JD'      , default=None)

        # CCD DETAILS
        self.ccdtemp        = self.header.get('CCD-TEMP', default=None)
        self.x_max          = self.header.get('NAXIS1'  , default=None)
        self.y_max          = self.header.get('NAXIS2'  , default=None)

        # TELESCOPE DETAILS
        self.latitude       = self.header.get('LAT-OBS' , default=None)
        self.longitude      = self.header.get('LONG-OBS', default=None)
        self.altitude       = self.header.get('ALT-OBS' , default=None)
        self.filter         = self.header.get('FILTER'  , default=None)
        self.focal_length   = self.header.get('FOCALLEN', default=None)
        self.color_band     = self.header.get('CLRBAND' , default=None)

        # SKY DETAILS
        self.airmass        = self.header.get('AIRMASS' , default=None)
        self.RA             = self.header.get('RA'      , default=None)
        self.DEC            = self.hedaer.get('DEC'     , default=None)

        