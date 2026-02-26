import xarray as xr
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

def cal_BT(IR):
    IR = IR*0.01+200
    IR = IR-273.15
    return IR

def gen_file_list(path):
    file_list = sorted(glob.glob(path+"*.nc"))
    return file_list

def load_dataset(path, jeddah_lat=21.5, jeddah_lon=39.2):
    """Find the lowest BT
    """
    min_temp = np.inf
    min_file = None
    file_list = gen_file_list(path)
    for file_path in file_list:
        # read dataset
        ds = xr.open_dataset(file_path)
        bt = cal_BT(ds['irwin_cdr']).isel(lat=slice(None, None, -1))

        # Jeddah
        bt_point = bt.sel(lat=jeddah_lat, lon=jeddah_lon, method="nearest")

        # Minimum BT in the region
        region_min = bt_point.values
        if region_min < min_temp:
            min_temp = region_min
            min_file = file_path

        ds.close()

    return min_file


def calculate_rainfall_rate(bt_celsius):
    """
    Calculate rainfall rate from brightness temperature
    using the AutoEstimator relationship.
    """

    # --- Convert to Kelvin ---
    bt_kelvin = bt_celsius + 273.15

    # --- AutoEstimator constants ---
    A = 1.1183e11      # mm h^-1
    b = 3.6382e-2      # K^-1
    c = 1.2

    # --- Compute rainfall rate ---
    rainfall_rate = A * np.exp(-b * (bt_kelvin ** c))

    return rainfall_rate

def plot_cumulative_rainfall(path, jeddah_lat=21.5, jeddah_lon=39.2):

    file_list = gen_file_list(path)

    if len(file_list) == 0:
        raise ValueError("No NetCDF files found in the specified directory.")

    time_list = ['00 UTC', '03 UTC', '06 UTC', '09 UTC', '12 UTC']
    dt = 3  

    cumulative_value = 0  
    cumulative_rain_list = []

    max_value = -np.inf
    max_file = None

    for file in file_list:

        ds = xr.open_dataset(file)

        # Brightness Temperature (BT)
        bt = cal_BT(ds['irwin_cdr']).isel(lat=slice(None, None, -1))

        # Jeddah
        bt_point = bt.sel(lat=jeddah_lat,
                          lon=jeddah_lon,
                          method="nearest")

        # Calculate rainfall rate
        rain = calculate_rainfall_rate(bt_point)

        
        rain_value = float(rain.values)

        # Cumulate rainfall
        rain_amount = rain_value * dt
        cumulative_value += rain_amount

        
        cumulative_rain_list.append(cumulative_value)

        # find max rainfall
        if rain_value > max_value:
            max_value = rain_value
            max_file = file

        ds.close()

    plt.figure()
    plt.plot(time_list, cumulative_rain_list, marker='o')
    plt.xlabel("Time (UTC)")
    plt.ylabel("Cumulative Rainfall (mm)")
    plt.title("Cumulative Rainfall at Jeddah")
    
    plt.savefig(path+'cumulative_rainfall.png', dpi=300)
    plt.show()

    return max_file