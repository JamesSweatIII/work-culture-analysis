from pymongo import MongoClient
import pandas as pd
import os

uri = ""

# Connect to your cluster
client = MongoClient(uri)
db = client["glassdoor-project"]

# Define the folder containing cleaned CSV files
cleaned_reviews_folder = "./glassdoor-data/cleaned-reviews"

# Loop through each CSV file in the folder
for filename in os.listdir(cleaned_reviews_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(cleaned_reviews_folder, filename)
        print(f"Processing file: {file_path}")
        
        # Load the CSV file
        df = pd.read_csv(file_path)
        records = df.to_dict(orient="records")
        
        # Determine the company name from the first record
        if records:
            company_name = records[0].get("company", "unknown").replace(" ", "_").lower()
            collection = db[company_name]  # Use the company name as the collection name
            
            # Insert records into the collection
            collection.insert_many(records)
            print(f"Inserted {len(records)} records into the '{company_name}' collection.")
        else:
            print(f"No records found in {filename}. Skipping.")
