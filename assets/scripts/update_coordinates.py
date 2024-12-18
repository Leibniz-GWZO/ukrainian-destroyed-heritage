import pandas as pd

# Load the metadata and coordinates CSV files
metadata_file = '_data/destroyed_ukr_metadata.csv'
coordinates_file = 'data_backups/destroyed_ukr_coordinates.csv'

# Read the metadata CSV into a DataFrame
metadata_df = pd.read_csv(metadata_file)

# Read the coordinates CSV into a DataFrame
coordinates_df = pd.read_csv(coordinates_file)

# Merge the metadata with the coordinates using 'objectid' as the key
# This will update latitude and longitude for matching objectids
updated_metadata_df = metadata_df.merge(
    coordinates_df,
    on='objectid',
    how='left',
    suffixes=('', '_coord')
)

# Use the coordinates from the coordinates file to update the metadata
updated_metadata_df['latitude'] = updated_metadata_df['latitude_coord'].combine_first(updated_metadata_df['latitude'])
updated_metadata_df['longitude'] = updated_metadata_df['longitude_coord'].combine_first(updated_metadata_df['longitude'])

# Drop the temporary latitude_coord and longitude_coord columns
updated_metadata_df = updated_metadata_df.drop(columns=['latitude_coord', 'longitude_coord'])

# Save the updated metadata to the same CSV file
updated_metadata_df.to_csv(metadata_file, index=False)

print("Coordinates updated successfully in 'destroyed_ukr_metadata.csv'.")
