### Assignment 1: Visualizing SRTM Elevation Data
## import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr


dset = xr.open_dataset('N21E039.SRTMGL1_NC.nc')           # load the SRTM data
#pdb.set_trace()                                          # add breakpoint here if needed

DEM = np.array(dset.variables['SRTMGL1_DEM'])             # extract the elevation data as a numpy array
dset.close()                                              # close the dataset
#pdb.set_trace()                                          # add breakpoint here if needed

plt.imshow(DEM)                                           # visualize the DEM using imshow
cbar = plt.colorbar()
cbar.set_label('Elevation (m asl)')
plt.savefig('assignment_1.png', dpi=300)                  # save the figure as a PNG file
plt.show()