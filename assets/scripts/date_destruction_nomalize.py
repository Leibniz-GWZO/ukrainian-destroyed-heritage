import pandas as pd
import re
from datetime import datetime

def normalize_date(date_str):
    """
    Normalize a date string to ISO format (YYYY-MM-DD if full date is provided, or just YYYY if only year is given).
    For ranges, pick the first year. For ambiguous values, approximate as best as possible.
    """
    try:
        if pd.isnull(date_str) or not isinstance(date_str, str):
            return None  # Return None for invalid or missing dates

        # Handle exact dates in day.month.year format
        if re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_str):
            return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
        
        # Handle exact years
        if re.match(r"^\d{4}$", date_str):
            return f"{date_str}"

        # Handle year ranges like "1900-1901"
        if re.match(r"^\d{4}-\d{4}$", date_str):
            start_year = date_str.split("-")[0]
            return f"{start_year}"

        # Handle year and decade approximations like "1950-s"
        if re.match(r"^\d{4}-s$", date_str):
            decade = date_str.split("-")[0]
            return f"{decade}"

        # Handle complex ranges like "1804-1808, 1999-2003"
        if re.match(r"^(\d{4}-\d{4})(, \d{4}-\d{4})*$", date_str):
            first_range = date_str.split(",")[0]
            start_year = first_range.split("-")[0]
            return f"{start_year}"

        # Handle approximate centuries like "XVIII century"
        if "century" in date_str.lower():
            century = re.search(r"(\d+)", date_str).group(1)
            start_year = (int(century) - 1) * 100 + 1
            return f"{start_year}"

        # Return None for unhandled formats
        return None
    except Exception:
        return None

# Load the CSV files
input_dates_file = "data_backups/destroyed_ukr_metadata - dates.csv"
existing_metadata_file = "_data/destroyed_ukr_metadata.csv"

# Read the input files into DataFrames
dates_df = pd.read_csv(input_dates_file)
metadata_df = pd.read_csv(existing_metadata_file)

# Normalize the date_destruction column in the new data
dates_df['date_destruction_normalized'] = dates_df['date_destruction'].apply(normalize_date)

# Merge normalized dates into the existing metadata
metadata_df = metadata_df.merge(
    dates_df[['objectid', 'date_destruction_normalized']],
    on='objectid',
    how='left'
)

# Preserve original `date_destruction` for `img_` objects if `date_destruction_normalized` is empty
def preserve_img_dates(row):
    if row['objectid'].startswith('img_'):
        if pd.isnull(row['date_destruction_normalized']) or row['date_destruction_normalized'] == "":
            return row['date_destruction']  # Retain original date
    return row['date_destruction_normalized']  # Use normalized date if available

# Apply the function to preserve `img_` object dates
metadata_df['date_destruction_normalized'] = metadata_df.apply(preserve_img_dates, axis=1)

# Map `obj_` object IDs to their normalized dates
objid_to_date = metadata_df[metadata_df['objectid'].str.startswith('obj_')].set_index('objectid')['date_destruction_normalized'].to_dict()

# Update the normalized `date_destruction` field for all rows
def update_normalized_date(row):
    # Normalize for all `obj_` objectids
    if row['objectid'].startswith('obj_'):
        return row['date_destruction_normalized']
    # For `img_` objects, inherit the parent's normalized date if `parentid` exists in `objid_to_date` and original `date_destruction` is not empty
    elif row['objectid'].startswith('img_') and pd.notnull(row['parentid']) and pd.notnull(row['date_destruction']) and row['date_destruction'] != "":
        return objid_to_date.get(row['parentid'], row['date_destruction'])
    # Otherwise, retain the original `date_destruction`
    return row['date_destruction']

# Apply the function to update the `date_destruction` column
metadata_df['date_destruction'] = metadata_df.apply(update_normalized_date, axis=1)

# Drop the temporary normalized column
if 'date_destruction_normalized' in metadata_df.columns:
    metadata_df = metadata_df.drop(columns=['date_destruction_normalized'])

# Save the updated metadata back to the file
output_file = "_data/destroyed_ukr_metadata.csv"
metadata_df.to_csv(output_file, index=False)

print(f"Updated metadata saved to {output_file}")
