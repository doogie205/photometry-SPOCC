from photutils.psf import IterativelySubtractedPSFPhotometry
from photutils.detection import IRAFStarFinder
from photutils.psf import IntegratedGaussianPRF, DAOGroup
from photutils.background import MMMBackground, MADStdBackgroundRMS
from astropy.modeling.fitting import LevMarLSQFitter
from astropy.stats import gaussian_sigma_to_fwhm
from astropy.io import fits
import matplotlib.pyplot as plt


##THIS IS THE SIGMA, CHANGE THIS FOR RESULTS
sigma_psf = 3.1

##THIS IS THE FILE, CHANGE THIS FOR RESULTS
with fits.open(r'/Users/phystastical/Desktop/BB2/script/twomass-j.fits') as hdul:
    image = hdul[0].data

bkgrms = MADStdBackgroundRMS()
std = bkgrms(image)


iraffind = IRAFStarFinder(threshold=3.5*std, fwhm=sigma_psf*gaussian_sigma_to_fwhm, minsep_fwhm=0.01, roundhi=5.0, roundlo=-5.0, sharplo=0.0, sharphi=2.0)
daogroup = DAOGroup(2.0*sigma_psf*gaussian_sigma_to_fwhm)

mmm_bkg = MMMBackground()
fitter = LevMarLSQFitter()
psf_model = IntegratedGaussianPRF(sigma=sigma_psf)
photometry = IterativelySubtractedPSFPhotometry(finder=iraffind, group_maker=daogroup, bkg_estimator=mmm_bkg, psf_model=psf_model, fitter=LevMarLSQFitter(), niters=1, fitshape=(11,11))
result_tab = photometry(image=image)
residual_image = photometry.get_residual_image()

#Plot images made#
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
plt.title('Raw Image')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
plt.subplot(1 ,2, 2)
plt.imshow(residual_image, cmap='viridis', aspect=1, interpolation='nearest', origin='lower')
plt.title('Residual Image')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)
plt.show()
phot_results = photometry(image)
print(phot_results['x_fit', 'y_fit', 'flux_fit'])



