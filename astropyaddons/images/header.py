from astropy.io import fits

class Header:
    """
    Header obtained from FITSImage. Extracts useful information
    and keeps it tidy in its own class.

    Parameters:
     - `header`: `astropy.io.fits.header.Header` object
    """
    def __init__(self, header: fits.header.Header):
        self.header: fits.header.Header = header
        
        ### Extracting useful values.

        # GENERAL OBSERVATION DETAILS
        self.exptime        = header.get('EXPTIME' , default=None)
        self.datetime       = header.get('DATE-OBS', default=None)
        self.JD             = header.get('JD'      , default=None)

        # CCD DETAILS
        self.ccdtemp        = header.get('CCD-TEMP', default=None)
        self.size_x         = header.get('NAXIS1'  , default=None)
        self.size_y         = header.get('NAXIS2'  , default=None)

        # TELESCOPE DETAILS
        self.latitude       = header.get('LAT-OBS' , default=None)
        self.longitude      = header.get('LONG-OBS', default=None)
        self.altitude       = header.get('ALT-OBS' , default=None)
        self.filter         = header.get('FILTER'  , default=None)
        self.focal_length   = header.get('FOCALLEN', default=None)
        self.color_band     = header.get('CLRBAND' , default=None)

        # SKY DETAILS
        self.airmass        = header.get('AIRMASS' , default=None)
        self.RA             = header.get('RA'      , default=None)
        self.DEC            = header.get('DEC'     , default=None)

        