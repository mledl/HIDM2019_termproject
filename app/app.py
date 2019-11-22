import pandas as pd

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

# variables that configure the program
arrest_dataset_path = "../data/Arrest_Data_from_2010_to_Present.csv"
trip_dataset_path = "../data/Metro_Bike_Share_Trip_Data.csv"
geolocation_data_path = "../data/Bikelanes.geojson"


# read the csv files
arrest_df = pd.read_csv(arrest_dataset_path, sep=',')
trip_df = pd.read_csv(trip_dataset_path, sep=',')

# quick statistics of the dataframes
print("\n")
arrest_df.info()
print("\n\n")
trip_df.info()
print("\n")

# print rows containing nan
arrest_nan_df = arrest_df[arrest_df.isna().any(axis=1)]
print(arrest_nan_df)
