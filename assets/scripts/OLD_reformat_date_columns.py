import pandas as pd
import re
from datetime import datetime

# Load your CSV file
file_path = '_data/destroyed_ukr_metadata.csv'
df = pd.read_csv(file_path)

# Function to clean and reformat dates
def clean_date(date):
    # Handle empty or NaN values
    if pd.isnull(date) or date == '':
        return ''

    # Handle multiple date ranges (e.g., "1804-1808, 1999-2003" -> "1804")
    if ',' in date:
        date = date.split(',')[0].strip()  # Take only the first range

    # Handle date ranges, e.g., "1900-1901" -> "1900"
    if re.match(r'^\d{4}-\d{4}$', date):
        return date.split('-')[0]

    # Handle approximate decades (e.g., "1950-s" -> "1950")
    if re.match(r'^\d{4}-s$', date):
        return date.replace('-s', '0')

    # Handle centuries (e.g., "18th century" -> "1800")
    century_match = re.match(r'(\d{1,2})(th|st|nd|rd)? century', date, re.IGNORECASE)
    if century_match:
        century = int(century_match.group(1))
        year = (century - 1) * 100  # Convert "18th century" to "1800"
        return str(year)

    # Handle exact dates in dd.mm.yyyy or mm/dd/yyyy formats
    try:
        if re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
            return datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
        elif re.match(r'^\d{2}/\d{2}/\d{4}$', date):
            return datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return ''  # Skip malformed date formats

    # Handle year-only or partial dates (e.g., "yyyy-mm" or "yyyy")
    if re.match(r'^\d{4}-\d{2}$', date):  # Format "yyyy-mm"
        return date
    elif re.match(r'^\d{4}$', date):  # Format "yyyy"
        return date

    # Return as-is if no other rules matched
    return date

# Apply the function to each date column
df['date_construction'] = df['date_construction'].apply(clean_date)
df['date_destruction'] = df['date_destruction'].apply(clean_date)

# Save the cleaned DataFrame
df.to_csv('_data/destroyed_ukr_metadata.csv', index=False)
print("Dates have been cleaned and saved to '_data/destroyed_ukr_metadata.csv'")