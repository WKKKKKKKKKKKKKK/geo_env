import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr

dset=xr.open_dataset('N21E039.SRTMGL1_NC.nc')

DEM = np.array(dset.variables["SRTMGL1_DEM"])

plt.imshow(DEM)
cbar = plt.colorbar()
cbar.set_label('Elevation (m asl)')
plt.show()