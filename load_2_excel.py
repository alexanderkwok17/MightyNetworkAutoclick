import os
import re
import pandas as pd
from datetime import datetime

# Define the directory containing the Excel files
download_directory = "/Users/alexanderkwok/Downloads"

# Define the regex pattern for matching file names
pattern = r"Network_Amplify_Australia_members_(\w+)_(\d{1,2})_(\d{4})_(\d{4}).xlsx"

# Initialize an empty list to store the dataframes
dataframes = []

# Crawl the download directory for matching files
for filename in os.listdir(download_directory):
    match = re.match(pattern, filename)
    if match:
        # Extract the date components from the file name
        month, day, year, time = match.groups()
        
        # Construct the full file path
        file_path = os.path.join(download_directory, filename)
        
        # Load the Excel file into a pandas dataframe
        df = pd.read_excel(file_path)
        
        # Convert the extracted date components into a datetime object
        load_datetime = datetime.strptime(f"{year} {month} {day} {time}", "%Y %B %d %H%M")
        
        # Add the Load_date column with the corresponding datetime
        df['Load_date'] = load_datetime
        
        # Append the dataframe to the list
        dataframes.append(df)

# Now you have all dataframes loaded with the Load_date column
# You can concatenate them if needed:
# all_data = pd.concat(dataframes, ignore_index=True)

# Merge all dataframes into a single dataframe
if dataframes:
    path = "/Users/alexanderkwok/Library/CloudStorage/OneDrive-Personal/Amplify data load/"
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    # Group by 'Join_date' and count distinct values in 'Member_ID'
    distinct_count = merged_df.groupby('Join Date')['Member ID'].nunique().reset_index()

    # Rename the columns for clarity
    distinct_count.columns = ['Join_date', 'Distinct_Member_Count']

    # Define the output file path
    output_file = f"{path}distinct_member_count.xlsx"

    # Write the result to an Excel file
    distinct_count.to_excel(output_file, index=False)

    print(f"Distinct member count written to {output_file}")
     
    # Define the output file path
    output_file = f"{path}merged_data.xlsx"
    
    # Write the merged dataframe to a new Excel file
    merged_df.to_excel(output_file, index=False)
    
    print(f"Merged data written to {output_file}")
else:
    print("No matching files found to merge.")