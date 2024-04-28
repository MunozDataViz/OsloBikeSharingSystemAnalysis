import pandas as pd
import os

""" 
Function to:
    1. Read filers from the trips folder
    2. Concate them into a single Dataframe
    3. Select the information from the stations
    4. Save the result to an Excel File
"""

def process_files(folder_path, columns_to_select, output_file):
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
    
    # Select certain columns
    combined_df = combined_df[columns_to_select]
    
    # Save the DataFrame to an Excel file
    combined_df.to_csv(output_file, index=False)
    
    print("File saved successfully.")

# Input Information    
folder_path = '/Users/victormunoz/Documents/GitHub/OsloBikeSharingSystemAnalytics/data/01 raw/bikeTrips'
columns_to_select = ['start_station_id',	'end_station_id', 'started_at',	'ended_at']  
output_file = '/Users/victormunoz/Documents/GitHub/OsloBikeSharingSystemAnalytics/data/02 processed/stations.csv'  

process_files(folder_path, columns_to_select, output_file)