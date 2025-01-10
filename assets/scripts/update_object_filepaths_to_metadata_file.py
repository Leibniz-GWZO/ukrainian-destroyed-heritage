import csv
import os

# File paths
source_csv = 'objects/object_list.csv'
dest_csv = '_data/destroyed_ukr_metadata.csv'

# Columns to update
columns_to_update = ['object_location', 'image_small', 'image_thumb']

# Read source CSV into a dictionary keyed by 'filename' without extension
source_data = {}
with open(source_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename = row['filename']
        # Remove file extension
        key = os.path.splitext(filename)[0]
        source_data[key] = row

# Read destination CSV into a list of dictionaries
with open(dest_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    dest_fieldnames = reader.fieldnames
    dest_data = [row for row in reader]

# Update destination data
for row in dest_data:
    key = row['identifier']
    if key in source_data:
        source_row = source_data[key]
        for col in columns_to_update:
            if col in source_row:
                row[col] = source_row[col]
    else:
        print(f"No match found for identifier: {key}")

# Write updated data back to destination CSV
with open(dest_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=dest_fieldnames)
    writer.writeheader()
    writer.writerows(dest_data)

print("CSV update completed successfully.")