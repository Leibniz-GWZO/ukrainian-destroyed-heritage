import pandas as pd

# File paths
input_file = '_data/destroyed_ukr_metadata.csv'
update_file = 'data_backups/processed_lectorate_corrections.csv'
output_file = '_data/destroyed_ukr_metadata.csv'

# Load the input and update DataFrames
df_combined = pd.read_csv(input_file)
df_updates = pd.read_csv(update_file)

# Merge the updates into the combined DataFrame
# Assuming 'objectid' is the primary key used for matching
key_column = 'objectid'
if key_column in df_combined.columns and key_column in df_updates.columns:
    df_combined.set_index(key_column, inplace=True)
    df_updates.set_index(key_column, inplace=True)

    # Update matching columns
    for column in df_updates.columns:
        if column in df_combined.columns:
            df_combined[column].update(df_updates[column])

    # Reset the index to save the DataFrame
    df_combined.reset_index(inplace=True)
else:
    print(f"Key column '{key_column}' is missing in one of the files.")

# Reorder columns to match the desired order
column_order = [
    'objectid', 'parentid', 'title', 'architect', 'credits', 'credits_before', 'credits_after',
    'caption_before', 'caption_after', 'date_construction', 'date_destruction', 'description', 'subsection',
    'location', 'latitude', 'longitude', 'source', 'identifier', 'type', 'format', 'language', 'rights',
    'rightsstatement', 'display_template', 'object_location', 'image_small', 'image_thumb', 'caption', 'notes',
    'region', 'image_alt_text', 'object_transcript'
]
for col in column_order:
    if col not in df_combined.columns:
        df_combined[col] = ''

df_combined = df_combined[column_order]

# Fix identifiers
def fix_children_identifier(identifier):
    if pd.notnull(identifier):
        return identifier.replace("children's", "childrens")
    return identifier

df_combined['identifier'] = df_combined['identifier'].apply(fix_children_identifier)

# Fill NaN values with empty strings
df_combined = df_combined.fillna('')

# Save the updated DataFrame to a new CSV file
df_combined.to_csv(output_file, index=False)

print(f"Processing complete. The lectorate updated data has been saved to '{output_file}'.")
