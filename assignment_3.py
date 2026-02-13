import tools
import matplotlib.pyplot as plt

#### Part 1: Read and plot ISD data ####
df_isd = tools.read_isd_csv('41024099999.csv')
plot = df_isd.plot(title="ISD data for Jeddah")
plt.show()

### Part 2: Calculate heat index and analyze ####
# HI = heat index
df_isd['RH'] = tools.dewpoint_to_rh(df_isd['DEW'].values, df_isd['TMP'].values)
df_isd['HI'] = tools.gen_heat_index(df_isd['TMP'].values, df_isd['RH'].values)

#The highest HI
df_isd['HI'].max()

#The index of the highest HI
df_isd['HI'].idxmax()

#The corresponding temperature and relative humidity of the highest HI
df_isd.loc[["2024-08-10 11:00:00"]]

# Calculate daily HI
dailyHI=df_isd.resample('D').mean()
dailyHI['RH'] = tools.dewpoint_to_rh(dailyHI['DEW'], dailyHI['TMP'])
dailyHI['HI'] = tools.gen_heat_index(dailyHI['TMP'], dailyHI['RH'])

## HItimeseries
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(dailyHI.index, dailyHI['HI'], marker='o', markersize=3)
ax.set_title("Daily mean heat index")
ax.set_xlabel("Date")
ax.set_ylabel("Heat Index (°C)")
plt.savefig('daily_heat_index.png', dpi=300, bbox_inches='tight')
plt.show()

### Part 3 ###
dailyHI2=df_isd.resample('D').mean()
dailyHI2['RH'] = tools.dewpoint_to_rh(dailyHI2['DEW'], dailyHI2['TMP']+2)
dailyHI2['HI'] = tools.gen_heat_index(dailyHI2['TMP']+2, dailyHI2['RH'])

diff=dailyHI2['HI'].max() - dailyHI['HI'].max()
print(diff)