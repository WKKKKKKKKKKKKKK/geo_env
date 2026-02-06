###### Part 1  #####
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr


dset=xr.open_dataset('tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_195001-201412.nc')
#pdb.set_trace()


###### Part 2 ####
dset.keys()

print(dset['tas']) # raster
print(dset['tas'].dtype)

###### Part 3 ######
dsethist=xr.open_dataset('tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc')
mean1850_1900 = np.mean(dsethist['tas'].sel(time=slice('18500101','19001231')), axis=0) # select time from 1850-01-01 to 1900-12-31, and calculate the mean along time dimension
mean1850_1900 = np.array(mean1850_1900)

print(mean1850_1900.shape, mean1850_1900.dtype)


def meansspT(filepath):
    dset = xr.open_dataset(filepath)
    mean2071_2100 = np.mean(dset['tas'].sel(time=slice('20710101','21001231')), axis=0)
    mean2071_2100 = np.array(mean2071_2100)
    return mean2071_2100

path='D:/KAUST/semster2/geo_env_modelling/assignment2/Climate_Model_Data/' # change to your path
file=['tas_Amon_GFDL-ESM4_ssp119_r1i1p1f1_gr1_201501-210012.nc',
      'tas_Amon_GFDL-ESM4_ssp245_r1i1p1f1_gr1_201501-210012.nc',
      'tas_Amon_GFDL-ESM4_ssp585_r1i1p1f1_gr1_201501-210012.nc']
mean=[]
for f in file:
    mean.append(meansspT(path+f))


diffssp119=mean[0]-mean1850_1900
diffssp245=mean[1]-mean1850_1900
diffssp585=mean[2]-mean1850_1900


###plot
mean119 = np.nanmean(diffssp119)
mean245 = np.nanmean(diffssp245)
mean585 = np.nanmean(diffssp585)


fig, axs = plt.subplots(1, 3, figsize=(20, 8))

vmin = min(diffssp119.min(), diffssp245.min(), diffssp585.min())
vmax = max(diffssp119.max(), diffssp245.max(), diffssp585.max())

cmap = "Reds"  

im1 = axs[0].imshow(diffssp119,
                    extent=[dset.lon.min(), dset.lon.max(), dset.lat.min(), dset.lat.max()],
                    cmap=cmap, vmin=vmin, vmax=vmax)
axs[0].set_title('SSP119', fontsize=16)
axs[0].set_xlabel('Longitude(°E)', fontsize=14)
axs[0].set_ylabel('Latitude(°N)', fontsize=14)
axs[0].tick_params(labelsize=12)
axs[0].text(0.02, 0.95, f"Mean = {mean119:.2f} K",
            transform=axs[0].transAxes, fontsize=14,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

im2 = axs[1].imshow(diffssp245,
                    extent=[dset.lon.min(), dset.lon.max(), dset.lat.min(), dset.lat.max()],
                    cmap=cmap, vmin=vmin, vmax=vmax)
axs[1].set_title('SSP245', fontsize=16)
axs[1].set_xlabel('Longitude(°E)', fontsize=14)
axs[1].set_ylabel('Latitude(°N)', fontsize=14)
axs[1].text(0.02, 0.95, f"Mean = {mean245:.2f} K",
            transform=axs[1].transAxes, fontsize=14,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
axs[1].tick_params(labelsize=12)

cbar = fig.colorbar(im1, ax=axs, orientation='horizontal', fraction=0.046, pad=0.1)
cbar.set_label('Temperature Difference (K)', fontsize=14)
cbar.ax.tick_params(labelsize=12)

plt.savefig('temperature_difference.png', dpi=300)
plt.show()