import pandas as pd

# Read the CSV file
def process_csv(input_file, output_file):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(input_file)

        # Ensure the column 'title' exists
        if 'title' not in df.columns:
            print("The 'title' column is missing in the input CSV file.")
            return

        # Process the 'title' column
        df['title'] = df['title'].apply(lambda x: x.split('-', 1)[1].strip() if '-' in x else x)

        # Save the updated DataFrame to a new CSV file
        df.to_csv(output_file, index=False)

        print(f"Processed CSV saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output file paths
input_file = 'data_backups/lectorate_corrections.csv'
output_file = 'data_backups/processed_lectorate_corrections.csv'

# Process the CSV file
process_csv(input_file, output_file)
