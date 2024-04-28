import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('/Users/victormunoz/Documents/GitHub/OsloBikeSharingSystemAnalytics/data/02 processed/allTrips.csv')  


# Convert 'started_at' and 'ended_at' columns to datetime
df['started_at'] = pd.to_datetime(df['started_at'], format='%Y-%m-%d %H:%M:%S.%f%z', errors='coerce')
df['ended_at'] = pd.to_datetime(df['ended_at'], format='%Y-%m-%d %H:%M:%S.%f%z', errors='coerce')

# Drop rows with missing datetime values
df.dropna(subset=['started_at', 'ended_at'], inplace=True)

# Extract date and hour information for 'started_at'
df['start_date'] = df['started_at'].dt.date
df['start_hour'] = df['started_at'].dt.hour

# Extract date and hour information for 'ended_at'
df['end_date'] = df['ended_at'].dt.date
df['end_hour'] = df['ended_at'].dt.hour

# Create a complete set of all unique combinations of station IDs, dates, and hours
stations = set(df['start_station_id'].unique()) | set(df['end_station_id'].unique())
dates = set(df['start_date'].unique()) | set(df['end_date'].unique())
hours = set(df['start_hour'].unique()) | set(df['end_hour'].unique())
station_date_hour_combinations = [(station_id, date, hour) for station_id in stations for date in dates for hour in hours]

# Create DataFrames for inflow and outflow
outflow = df.groupby(['start_station_id', 'start_date', 'start_hour']).size().reset_index(name='outflow')
inflow = df.groupby(['end_station_id', 'end_date', 'end_hour']).size().reset_index(name='inflow')

# Merge inflow and outflow with the complete set of station-date-hour combinations
net_flow = pd.DataFrame(station_date_hour_combinations, columns=['station_id', 'date', 'hour'])
net_flow = pd.merge(net_flow, outflow, how='left', left_on=['station_id', 'date', 'hour'], right_on=['start_station_id', 'start_date', 'start_hour'])
net_flow = pd.merge(net_flow, inflow, how='left', left_on=['station_id', 'date', 'hour'], right_on=['end_station_id', 'end_date', 'end_hour'])

# Fill NaN values with 0
net_flow['inflow'].fillna(0, inplace=True)
net_flow['outflow'].fillna(0, inplace=True)

# Calculate net flow
net_flow['net_flow'] = net_flow['inflow'] - net_flow['outflow']

# Select relevant columns
net_flow = net_flow[['station_id', 'date', 'hour', 'inflow', 'outflow', 'net_flow']]

# Save the result to a CSV file
net_flow.to_csv('/Users/victormunoz/Documents/GitHub/OsloBikeSharingSystemAnalytics/data/02 processed/netFlow.csv', index=False)

print("Result saved as netFlow.csv")