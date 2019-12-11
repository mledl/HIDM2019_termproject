import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import geopandas as gpd
import wordcloud
import os

##################################################################################
# datasets:
# ../data/Arrest_Data_from_2010_to_Present.csv
#       dataset  contains 1.31M records and each record consists of 17 features.
#       The most interesting features are Arrest date, Time, Area Name, Location,
#       Charge Group Code, Arrest Type Code.
#
# ../data/Metro_Bike_Share_Trip_Data.csv
#       dataset contains 132k records and each record consists of 16 features.
#       The most interesting features are Starting Station Latitude, Starting
#       Station Longitude, Ending Station Latitude, Ending Station Longitude.
# ../data/Bikelanes.geojson
#       map is a set of geospatial data which contains information about bike
#       lanes. It is possible to export this data in different formats (KML, KMZ,
#       shapefile, json etc).
###################################################################################
# ../data/Arrest_Data_from_2010_to_Present.csv - Feature Sample:
# Report ID = 4248313
# Arrest Date = 02/24/2015
# Time = 1310
# Area ID = 20
# Area Name = Olympic
# Reporting District = 2022
# Age = 37
# Sex Code = M
# Descent Code = H
# Charge Group Code = 05
# Charge Group Description = Burglary
# Arrest Type Code = F
# Charge = 459PC
# Charge Description = BURGLARY
# Address = 5TH
# Cross Street = WILTON
# Location = (34.0653, -118.314)
###################################################################################
# ../data/Metro_Bike_Share_Trip_Data.csv - Feature Sample:
# Trip ID = 112,531,532
# Duration = 1,500
# Start Time = 11/06/2016 02:34:00 PM
# End Time = 11/06/2016 02:59:00 PM
# Starting Station ID =
# Starting Station Latitude =
# Starting Station Longitude =
# Ending Station ID = 3,034
# Ending Station Latitude =34.042061
# Ending Station Longitude = -118.263382
# Bike ID = 5,997
# Plan Duration = 30
# Trip Route Category = One Way
# Passholder Type = Monthly Pass
# Starting Lat-Long =
# Ending Lat-Long = (34.042061, -118.263382)
###################################################################################
# variables that configure the program
###################################################################################

# paths to datasets
arrest_dataset_path = "../data/Arrest_Data_from_2010_to_Present.csv"
trip_dataset_path = "../data/Metro_Bike_Share_Trip_Data.csv"
geolocation_data_path = "../data/Bikelanes.geojson"

# result paths
results_save_path = os.path.abspath("..") + os.path.sep + "data" + os.path.sep + "results" + os.path.sep

###################################################################################

###################################################################################
# Data exploration
###################################################################################
# read the csv files and geojson
df_arrest = pd.read_csv(arrest_dataset_path, sep=',')
df_trip = pd.read_csv(trip_dataset_path, sep=',')
df_geo = gpd.read_file(geolocation_data_path)

# quick statistics of the dataframes
print("\n")
df_arrest.info()
print("\n\n")
df_trip.info()
print("\n")

# print rows containing nan
arrest_nan_df = df_arrest[df_arrest.isna().any(axis=1)]
print(arrest_nan_df)


###################################################################################
# Data preprocessing
###################################################################################
# extract columns that we need for analysis
arrest_cols = ['Arrest Date', 'Time', 'Area Name', 'Age', 'Sex Code', 'Descent Code', 'Charge Group Description',
               'Charge Description', 'Address', 'Cross Street', 'Location']
trip_cols = ['Start Time', 'End Time', 'Starting Station ID', 'Starting Station Latitude', 'Starting Station Longitude',
             'Ending Station ID', 'Ending Station Latitude', 'Ending Station Longitude', 'Trip Route Category']
df_arrest = df_arrest[arrest_cols]
df_trip = df_trip[trip_cols]

# replace Nan in Charge Group Description and Charge Description with Unknown/UNKNOWN
df_arrest['Charge Group Description'].fillna('Unknown', inplace=True)
df_arrest['Charge Description'].fillna('UNKNOWN', inplace=True)

###################################################################################
# Analyse arrest dataset
###################################################################################
# most frequently committed crimes - wordcount
print(df_arrest['Charge Description'])
charge_desc_list = "".join(desc for desc in df_arrest['Charge Description'])
charge_group_desc_list = "".join(desc for desc in df_arrest['Charge Group Description'])

# establish the wordclouds
charge_desc_wc = wordcloud.WordCloud().generate(charge_desc_list)
plt.figure(figsize=[10, 10])
plt.imshow(charge_desc_wc, interpolation='bilinear')
plt.axis("off")
plt.savefig(results_save_path + "charge_description_wordcloud.png", format='png')

charge_group_desc_wc = wordcloud.WordCloud().generate(charge_group_desc_list)
plt.figure(figsize=[10, 10])
plt.imshow(charge_group_desc_wc, interpolation='bilinear')
plt.axis("off")
plt.savefig(results_save_path + "charge_group_description_wordcloud.png", format='png')

plt.show()

###################################################################################
