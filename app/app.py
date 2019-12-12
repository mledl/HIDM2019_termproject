import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
# import geopandas as gpd
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
#df_geo = gpd.read_file(geolocation_data_path)

# quick statistics before feature extraction and data cleaning
print("\n")
print("Datasets before preprocessing:\n")
df_arrest.info()
print("\n\n")
df_trip.info()
print("\n")

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

# drop rows according to missing values in important columns
df_arrest = df_arrest.dropna(subset=['Charge Group Description'])
df_trip = df_trip.dropna(subset=['Ending Station Latitude', 'Starting Station Latitude'])

# replace Nan in Charge Group Description and Charge Description with Unknown/UNKNOWN
df_arrest['Charge Group Description'].fillna('Unknown', inplace=True)
df_arrest['Charge Description'].fillna('UNKNOWN', inplace=True)

# replace missing arrest time with midday (1200)
df_arrest['Time'].fillna(1200, inplace=True)
df_arrest['Cross Street'].fillna('Unknown', inplace=True)

# quick summary of the data after preprocessing
print("\n")
print("Datasets after preprocessing:\n")
df_arrest.info()
print("\n\n")
df_trip.info()
print("\n")

###################################################################################
# Analyse arrest dataset
###################################################################################
def generate_wordcloud(column):
    # get list of words
    column_elems = "".join(desc for desc in df_arrest[column])

    # establish the wordclouds
    elems_wc = wordcloud.WordCloud().generate(column_elems)
    plt.figure(figsize=[10, 10])
    plt.imshow(elems_wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(results_save_path + "wordcloud_" + column.replace(" ", "_") + ".png", format='png')


def generate_histogram(name, bin_color, x, y, data, xlabel, ylabel):
    sb.set(style="whitegrid")
    f, ax = plt.subplots(figsize=(30, 15))
    sb.set_color_codes("pastel")
    sb.barplot(x=x, y=y, data=data, label="Total", color=bin_color)
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(ylabel=ylabel, xlabel=xlabel)
    sb.despine(left=True, bottom=True)
    plt.savefig(results_save_path + "histogram_" + name.replace(" ", "_") + ".png", format='png')


def generate_df_count(df_data, column):
    df_count = pd.DataFrame(df_data.groupby(column)\
                                          .size()
                                          .sort_values(ascending=False)\
                                          .rename('Counts')
                                          .reset_index())
    return df_count


# most frequently committed crimes - wordcount
#generate_wordcloud('Charge Description')
#generate_wordcloud('Charge Group Description')

# most frequently committed crimes - histograms
df_charge_group_desc_count = generate_df_count(df_arrest, 'Charge Group Description')
df_charge_desc_count = generate_df_count(df_arrest, 'Charge Description')


generate_histogram('Charge Group Description', 'b', 'Counts', 'Charge Group Description',
                   df_charge_group_desc_count.iloc[:10, :], 'Counts', 'Charge Group Description')
generate_histogram('Charge Description', 'b', 'Counts', 'Charge Description', df_charge_desc_count.iloc[:10, :],
                   'Counts', 'Charge Description')


###################################################################################
