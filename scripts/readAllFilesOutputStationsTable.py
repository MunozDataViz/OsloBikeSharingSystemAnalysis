import pandas as pd
import os

"""
Function to:
    1. Read all the files from the trips
    2. Concatenate them into a single dataframe
    3. Select the columns with the information of the station
        - Station ID
        - Station Name
        - Station Description
        - Station Latitutde
        - Station Longitude 
    4. Rename the columns
    5. Save the result into a CSV file
"""


def process_files(folder_path, other_columns, column_names, output_file):

    # List to hold individual DataFrames
    dfs = []
    
    # Iterate through each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):  
            file_path = os.path.join(folder_path, file_name)
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            # Append the DataFrame to the list
            dfs.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Concatenate start and end station columns into a single DataFrame
    start_station_columns = ['start_station_id', 'start_station_name', 'start_station_description', 'start_station_latitude', 'start_station_longitude']
    end_station_columns = ['end_station_id', 'end_station_name', 'end_station_description', 'end_station_latitude', 'end_station_longitude']
    station_df = combined_df[start_station_columns].copy()
    end_station_df = combined_df[end_station_columns].copy()
    end_station_df.columns = start_station_columns
    combined_df = pd.concat([station_df, end_station_df], axis=0, ignore_index=True)
    
    # Pivot the selected column
    pivot_df = combined_df.pivot_table(index='start_station_id', aggfunc='size').reset_index()
    pivot_df = pivot_df.drop(columns=[pivot_df.columns[1]])
    
    # Aggregate other columns as the last values
    for col in other_columns:
        pivot_df[col] = combined_df.groupby('start_station_id')[col].last().values
    
    # Rename the columns
    pivot_df.columns = column_names
    
    # Save the result to a CSV file without index
    pivot_df.to_csv(output_file, index=False)  # <- Set index=False here
    
    print("File saved successfully.")



# Inputs
folder_path = '/Users/victormunoz/Documents/GitHub/OsloBikeSharingSystemAnalytics/data/01 raw/bikeTrips' 
other_columns = ['start_station_name', 'start_station_description', 'start_station_latitude', 'start_station_longitude']  
column_names = ['station_id',	'station_name',	'station_description',	'station_latitude',	'station_longitude'] 
output_file = '/Users/victormunoz/Documents/GitHub/OsloBikeSharingSystemAnalytics/data/02 processed/stations.csv'  

process_files(folder_path, other_columns, column_names, output_file)