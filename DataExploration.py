import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize, CenteredNorm
import numpy as np
from os.path import join

from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.units import Quantity

def CropImage(image, centre, height, width):

	centre = SkyCoord(centre[0], centre[1], unit="deg")
	size = Quantity([height, width], unit="deg")

	return Cutout2D(image[0].data, centre, size, wcs=WCS(image[0].header))

def GetCutout(image, cutout):
	"""
	Get the cropped image from a cutout entry.
	"""
	return CropImage(image, (cutout[1], cutout[2]), abs(cutout[4]-cutout[8]), abs(cutout[3]-cutout[5]))

def ShowCutout(image, cutout):
	"""
	Plot a given cutout from the image
	"""

	# Cropping the image to the cutout box
	croppedImg = GetCutout(hdulImage, cutout)

	# Plotting the cropped image
	fig, ax = plt.subplots(subplot_kw=dict(projection=croppedImg.wcs))
	ax.imshow(croppedImg.data, cmap="plasma", norm=LogNorm())
	ax.set_xlabel("Right Ascension")
	ax.set_ylabel("Declination")
	
	return fig, ax

# Dictionary containing all data files
DataDict = {
	  "NIRH": "EUC_MER_BGSUB-MOSAIC-NIR-H_TILE102159484-39CF67_20241024T214009.099906Z_00.00.fits", 
	  "NIRJ": "EUC_MER_BGSUB-MOSAIC-NIR-J_TILE102159484-C026DB_20241024T213141.416722Z_00.00.fits", 
	  "NIRY": "EUC_MER_BGSUB-MOSAIC-NIR-Y_TILE102159484-A9CCA7_20241024T221227.957725Z_00.00.fits", 
	   "VIS": "EUC_MER_BGSUB-MOSAIC-VIS_TILE102159484-116033_20241025T015934.885975Z_00.00.fits", 
	   "CAT": "EUC_MER_FINAL-CAT_TILE102159484-EF6D85_20241026T003047.133877Z_00.00.fits", 
	"CUTOUT": "EUC_MER_FINAL-CUTOUTS-CAT_TILE102159484-73BCF1_20241025T145359.184204Z_00.00.fits", 
	 "MORPH": "EUC_MER_FINAL-MORPH-CAT_TILE102159484-AE979F_20241026T003045.182961Z_00.00.fits", 
	  "GSED": "EUC_PHZ_GALAXYSED__20241120T003959.957136Z_00.00.fits",
	"PHZCAT": "EUC_PHZ_PHZCAT__20241120T003850.158262Z_00.00.fits", 
	  "SSED": "EUC_PHZ_STARSED__20241120T003936.665995Z_00.00.fits", 
	"SPELIN":"EUC_SPE_WIDE-CAT-LIN-102159484_N_20241110T054343.637093Z_00.00.fits", 
	"SPEMOD": "EUC_SPE_WIDE-CAT-MOD-102159484_N_20241110T054509.870865Z_00.00.fits", 
	  "SPEZ": "EUC_SPE_WIDE-CAT-Z-102159484_N_20241110T054253.801351Z_00.00.fits"
}

# Which image to use
filt = "NIRH"

DATADIR = "Repository/SampleData/"

# Getting the cutouts and image
hdulCutouts = fits.open(join(DATADIR, f"{DataDict["CUTOUT"]}"))
hdulImage  = fits.open(join(DATADIR, f"{DataDict[filt]}"))
# hdulMorph = fits.open(join(DATADIR, f"{DataDict["MORPH"]}"))
hdulGSED = fits.open(join(DATADIR, f"{DataDict["GSED"]}"))
hdulSSED = fits.open(join(DATADIR, f"{DataDict["SSED"]}"))

# Looping through the cutouts
""" for cutout in hdulCutouts[1].data[0:100]:
	
	fig, ax = ShowCutout(hdulImage, cutout)
	plt.show() """

def GetSED(hdul, idx, EBounds=(4500, 10000), EStep=100):

	# Creating empty arrays
	flux = np.empty(55)
	fluxErr = np.empty(55)
	E = np.empty(55)
	EErr = np.ones(55) * EStep/2

	for i, energy in enumerate(range(EBounds[0], EBounds[1], EStep)):
		flux[i] = hdul[1].data[idx][f"FLUX_{energy}_{energy+EStep}"]
		fluxErr[i] = hdul[1].data[idx][f"FLUXERR_{energy}_{energy+EStep}"]
		E[i] = energy + EStep/2

	return E, EErr, flux, fluxErr


E, EErr, flux, fluxErr = GetSED(hdulGSED, 10)
numnan=0
i=0

GData = hdulGSED[1].data["FLUX_4500_4600"]
SData = hdulSSED[1].data["FLUX_4500_4600"]
count = np.count_nonzero((np.invert(np.isnan(GData)) & np.invert(np.isnan(SData))))
print(count)
idxs = np.arange(0, len(GData))

print(idxs[(np.invert(np.isnan(GData)) & np.invert(np.isnan(SData)))])
idxs = idxs[(np.invert(np.isnan(GData)) & np.invert(np.isnan(SData)))]

# for i in idxs:
	
# 	fig, ax = plt.subplots()
# 	E, EErr, flux, fluxErr = GetSED(hdulGSED, i)
# 	ax.plot(E, flux, label="Galaxy")
# 	E, EErr, flux, fluxErr = GetSED(hdulSSED, i)
# 	ax.plot(E, flux, label="Star")
# 	ax.set_xlabel("Wavelength (Angstroms)")
# 	ax.set_ylabel("Flux")
# 	ax.legend()

# 	fig.savefig(f"WeirdSEDS/{i}.png")
# 	plt.close()

print(len(SData) - np.count_nonzero(np.isnan(SData)))

i=247

fig, ax = plt.subplots()
E, EErr, flux, fluxErr = GetSED(hdulGSED, i)
ax.errorbar(
	E, flux, fluxErr, EErr, 
	label="Galaxy", fmt=".", 
	ms=1, c="k", capsize=2, elinewidth=0.5
)
E, EErr, flux, fluxErr = GetSED(hdulSSED, i)
ax.errorbar(
	E, flux, fluxErr, EErr, 
	label="Star", fmt=".", 
	ms=1, c="r", capsize=2, elinewidth=0.5
)
ax.set_xlabel("Wavelength (Angstroms)")
ax.set_ylabel("Flux")
ax.legend()

# plt.show()

ShowCutout(hdulImage, hdulCutouts[1].data[74])
plt.show()