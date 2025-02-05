import pandas as pd
import os
import re

# Read the CSV data into a DataFrame
df = pd.read_csv('data_backups/destroyed_ukr_metadata_full_RAW.csv', encoding='utf-8')

# Rename columns for clarity
df = df.rename(columns={
    'Unique identification name of the object photo (before destruction)': 'identifier_before',
    'Credits (photo before destruction)': 'credits_before',
    'Caption (photo before destruction)': 'caption_before',
    'Unique identification name of the object photo (after destruction)': 'identifier_after',
    'Credits (photo after destruction)': 'credits_after',
    'Caption (photo after destruction)': 'caption_after',
    'Subsection': 'subjects',
    'Name of the object / building': 'title',
    'Place / City Ukrainian name / English name': 'location',
    'Region (in English)': 'region',
    'Explanation text in English (about 50 words)': 'description',
    'architect': 'architect',
    'Date of construction': 'date_construction',
    'Date of destruction': 'date_destruction',
    'further remarks / information ?': 'notes'
})

# Function to clean filenames
def clean_filename(filename):
    # Convert to string
    filename = str(filename)
    # Remove special characters, replace spaces, hyphens, and dots with underscores
    filename = filename.replace(' ', '_').replace('-', '_').replace('.', '_')
    # Convert to lowercase
    filename = filename.lower()
    # Return the cleaned filename with .jpg extension
    return filename + '.jpg'

# Initialize counters for objectid
objectid_counter = 1

# Lists to store parent and child records
parent_records = []
child_records = []

for idx, row in df.iterrows():
    parent_objectid = f"obj_{objectid_counter:03d}"
    objectid_counter += 1

    # Modify title to include location at the beginning
    #parent_title = f"{row['location']} - {row['title']}"

    # Capitalize each word in the title
    parent_title = str(row['title']).title()
    
    # Create parent record
    parent = {
        'objectid': parent_objectid,
        'parentid': '',
        'title': parent_title,
        'architect': row['architect'],
        'credits': row['credits_before'],
        'credits_before': row['credits_before'],
        'credits_after': row['credits_after'],
        'caption_before': row['caption_before'],
        'caption_after': row['caption_after'],
        'date_construction': row['date_construction'],
        'date_destruction': row['date_destruction'],
        'description': row['description'],
        'subjects': row['subjects'],
        'location': row['location'],
        'latitude': '',
        'longitude': '',
        'source': '',
        'identifier': '',
        'type': 'record',
        'format': '',
        'language': '',
        'rights': '',
        'rightsstatement': '',
        'display_template': 'multiple',
        'object_location': '',
        'image_small': '',
        'image_thumb': '',
        'notes': row['notes'],
        'region': row['region'],
        'image_alt_text': '',
        'object_transcript': ''
    }

    # Use the 'before' image as the representative image for the parent if available
    if pd.notnull(row['identifier_before']):
        filename_before = clean_filename(row['identifier_before'])
        parent['identifier'] = filename_before.replace('.jpg', '')
    else:
        filename_after = clean_filename(row['identifier_after'])
        parent['identifier'] = filename_after.replace('.jpg', '')

    parent_records.append(parent)

    # Create child records for 'before' and 'after' images
    for image_type in ['before', 'after']:
        if pd.notnull(row[f'identifier_{image_type}']):
            child_objectid = f"img_{objectid_counter:03d}"
            objectid_counter += 1

            filename = clean_filename(row[f'identifier_{image_type}'])

            # Conditional logic for dates
            date_destruction = row['date_destruction'] if image_type == 'after' else ''
            date_construction = row['date_construction'] if image_type == 'before' else ''            
            caption_before = row['caption_before'] if image_type == 'before' else ''
            caption_after = row['caption_after'] if image_type == 'after' else ''
            credits_after = row['credits_after'] if image_type == 'after' else ''
            credits_before = row['credits_before'] if image_type == 'before' else ''

            # Modify title to include location at the beginning
            #child_title = f"{row['location']} - {row['title']}"

            # Capitalize each word in the title
            child_title = str(row['title']).title()

            child = {
                'objectid': child_objectid,
                'parentid': parent_objectid,
                'title': child_title,
                'architect': row['architect'],
                'credits': row[f'credits_{image_type}'] if pd.notnull(row[f'credits_{image_type}']) else '',
                'credits_before': credits_before,
                'credits_after': credits_after,
                'caption_before': caption_before,
                'caption_after': caption_after,
                'date_construction': date_construction,
                'date_destruction': date_destruction,
                'description': '',
                'subjects': '',
                'location': row['location'],
                'latitude': '',
                'longitude': '',
                'source': '',
                'identifier': filename.replace('.jpg', ''),
                'type': 'Image;StillImage',
                'format': 'image/jpeg',
                'language': '',
                'rights': '',
                'rightsstatement': '',
                'display_template': 'image',
                'object_location': '/objects/' + filename,
                'image_small': '/objects/small/' + filename.replace('.jpg', '_sm.jpg'),
                'image_thumb': '/objects/thumbs/' + filename.replace('.jpg', '_th.jpg'),
                'caption': row[f'caption_{image_type}'],
                'notes': '',
                'region': '',
                'image_alt_text': row[f'caption_{image_type}'],
                'object_transcript': ''
            }

            child_records.append(child)

# Combine parent and child records
combined_records = parent_records + child_records

# Convert to DataFrame
df_combined = pd.DataFrame(combined_records)

# Reorder columns to match your desired order
column_order = [
    'objectid', 'parentid', 'title', 'architect', 'credits', 'credits_before', 'credits_after',
    'caption_before', 'caption_after', 'date_construction', 'date_destruction', 'description', 'subjects',
    'location', 'latitude', 'longitude', 'source', 'identifier', 'type', 'format', 'language', 'rights',
    'rightsstatement', 'display_template', 'object_location', 'image_small', 'image_thumb', 'caption', 'notes',
    'region', 'image_alt_text', 'object_transcript'
]

# Ensure all columns are present
for col in column_order:
    if col not in df_combined.columns:
        df_combined[col] = ''

df_combined = df_combined[column_order]

# Function to fix identifiers
def fix_children_identifier(identifier):
    if pd.notnull(identifier):
        return identifier.replace("children's", "childrens")
    return identifier

# Apply the fix to relevant fields in the DataFrame
df_combined['identifier'] = df_combined['identifier'].apply(fix_children_identifier)

# Fill NaN values with empty strings
df_combined = df_combined.fillna('')

# Save the processed DataFrame to a new CSV file
df_combined.to_csv('_data/destroyed_ukr_metadata.csv', index=False)

print("Processing complete. The transformed data has been saved to '_data/destroyed_ukr_metadata.csv'.")
