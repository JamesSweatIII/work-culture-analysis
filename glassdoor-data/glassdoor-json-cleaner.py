import os
import json
import pandas as pd

# Define input and output folders
reviews_folder = "./glassdoor-data/reviews"
output_folder = "./glassdoor-data/cleaned-reviews"
os.makedirs(output_folder, exist_ok=True)

# Loop through each JSON file in the reviews folder
for filename in os.listdir(reviews_folder):
    if filename.endswith(".json"):
        input_path = os.path.join(reviews_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
        
        # Load the JSON file
        with open(input_path, "r", encoding="utf-8") as f:
            raw = json.load(f)  # list of dicts

        normalized_data = []

        # Normalize the data
        for r in raw:
            normalized = {
                "company": r["employer"]["shortName"] if r.get("employer") else None,
                "role": r["jobTitle"]["text"] if r.get("jobTitle") else None,
                "location": r["location"]["name"] if r.get("location") else None,
                "date": r["reviewDateTime"][:10] if r.get("reviewDateTime") else None,
                "rating": r.get("ratingOverall"),
                "review_title": r.get("summary", ""),
                "pros": r.get("pros", ""),
                "cons": r.get("cons", ""),
            }
            
            # Combine full text for embedding
            normalized["full_text"] = f"{normalized['review_title']}. {normalized['pros']}. {normalized['cons']}".strip()
            
            normalized_data.append(normalized)

        # Save to CSV
        df = pd.DataFrame(normalized_data)
        df.to_csv(output_path, index=False, encoding="utf-8")
        
        # Print the company name and number of rows in the CSV
        company_name = normalized_data[0]["company"] if normalized_data else "Unknown"
        print(f"Processed and saved: {company_name} reviews with {len(df)} rows")
