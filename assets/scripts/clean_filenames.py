import os
import re

# Function to clean filenames
def clean_filename(filename):
    # Convert to string
    filename = str(filename)
    # Remove '.jpg' from the end if it exists
    if filename.lower().endswith('.jpg'):
        filename = filename[:-4]
    # Split the filename and extension
    #name, ext = os.path.splitext(filename)
    name = filename
    # Remove special characters, replace spaces, hyphens, and dots with underscores
    name = name.replace(' ', '_').replace('-', '_').replace('.', '_')
    name = name.replace('okhtyrka_railway_railexpoua', 'okhtyrka_railway_railexpoua_com')
    #name = re.sub(r'[^\w\s-]', '', name)
    # Convert to lowercase
    name = name.lower()
    # Return the cleaned filename with .jpg extension
    return name + '.jpg'


# Path to the 'objects' folder
objects_folder = 'objects'  # Adjust this path if necessary

# Get a list of all files in the 'objects' folder
file_list = os.listdir(objects_folder)

# Create a set to keep track of new filenames to avoid duplicates
new_filenames = set()

# Process each file in the folder
for filename in file_list:
    # Only process .jpg files
    if filename.lower().endswith('.jpg'):
        original_path = os.path.join(objects_folder, filename)
        cleaned_name = clean_filename(filename)
        new_path = os.path.join(objects_folder, cleaned_name)

        # Check for potential conflicts
        if cleaned_name in new_filenames:
            print(f"Warning: The filename '{cleaned_name}' already exists. Skipping '{filename}'.")
            continue
        elif os.path.exists(new_path):
            print(f"Warning: The file '{new_path}' already exists on disk. Skipping '{filename}'.")
            continue
        else:
            # Rename the file
            os.rename(original_path, new_path)
            print(f"Renamed '{filename}' to '{cleaned_name}'")
            new_filenames.add(cleaned_name)
