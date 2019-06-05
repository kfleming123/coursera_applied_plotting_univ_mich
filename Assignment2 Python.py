
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[3]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[5]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
get_ipython().magic('matplotlib notebook')
file = "data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv"
file1 = pd.read_csv(file, index_col=0, skiprows=0)
file1.head()
# new data frame with split value columns 
new = file1['Date'].str.split('-', n = 1, expand = True)
file1['Temp'] = file1['Data_Value'] * .1
# making seperate first name column from new data frame 
file1['Year']= new[0] 
file1['Day']= new[1]
file1.drop(['Date', 'Data_Value'], axis=1, inplace = True)
# remove leap year:
file1 = file1[file1['Day'] != '02-29']
#split into 2005 - 2014 and 2015
file2 = file1[file1['Year'] == '2015']
file3 = file1[file1['Year'] != '2015']
#create 2005 - 2014 high lows
minmax = pd.DataFrame()
minmax['min'] = file3.groupby('Day')['Temp'].min()
minmax['max'] = file3.groupby('Day')['Temp'].max()
minmax.reset_index(inplace=True)
#find new highs in 2015
minmax15 = pd.DataFrame()
minmax15['min'] = file2.groupby('Day')['Temp'].min()
minmax15['max'] = file2.groupby('Day')['Temp'].max()
minmax15.reset_index(inplace=True)
minmax15['new_high'] = minmax15['max'].where(minmax15['max'] > minmax['max'])
minmax15['new_low'] = minmax15['min'].where(minmax15['min'] < minmax['min'])
minmax15

#Plot the figuer
plt.figure()
plt.title('New Daily Highs and Lows Ann Arbor, MI 2015 vs. 2005 - 2014')
#axes
ax = plt.gca()
# Set axis properties [xmin, xmax, ymin, ymax]
ax.axis([0,365,-40,45])
# x axis ticks
my_xticks = ['Jan','Feb','Mar','Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
x = [15, 45, 75, 105, 135, 165, 195, 225, 255, 285, 315, 345]
plt.xticks(x, my_xticks)
#y axis ticks
my_yticks = ['-40', '-20', '0', '20', '40']
y = [-40, -20, 0, 20, 40]
plt.yticks(y, my_yticks)
#plot min and max from 2005 to 2014
plt.plot(minmax['min'], '-', color='blue', alpha=0.25)
plt.plot(minmax['max'], '-', color='blue', alpha=0.25, label='_nolegend_')
ax.fill_between(range(len(minmax['min'])), 
                       minmax['max'], minmax['min'], 
                       facecolor='blue', 
                       alpha=0.25)
plt.plot(minmax15['new_high'], '.', color='r')
plt.plot(minmax15['new_low'], '.', color='b')
#Hide top and right spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#Label axes
plt.ylabel('$^\circ$ Celsius')
plt.xlabel('Month')
#Create a legend
plt.legend()
plt.legend(['2005 - 2014 Range', 'New High 2015', 'New Low 2015'], loc=8, frameon=False)


# ## 
