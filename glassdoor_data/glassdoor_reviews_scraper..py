import os
import json
from apify_client import ApifyClient

# Prompt the user for their Apify API token
api_token = input("Enter your Apify API token: ").strip()

# Initialize the ApifyClient with the provided API token
client = ApifyClient(api_token)

# Read URLs from the "urls.txt" file
urls_file_path = "./glassdoor_data/urls.txt"
if not os.path.exists(urls_file_path):
    print(f"Error: {urls_file_path} not found. Please create the file and add URLs (one per line).")
    exit()

with open(urls_file_path, "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file if line.strip()]

if not urls:
    print("Error: No URLs found in urls.txt. Please add URLs (one per line).")
    exit()

# Confirm output to the "reviews" folder
default_reviews_folder = "./glassdoor_data/reviews"
print(f"Results will be saved to the default folder: {default_reviews_folder}")

# Ensure the "reviews" folder exists
os.makedirs(default_reviews_folder, exist_ok=True)

# Loop through each URL and process it
for url in urls:
    print(f"Processing URL: {url}")

    # Prepare the Actor input for the current URL
    run_input = {
        "startUrls": [{"url": url}],
        "command": "reviews",
        "includes": [],
        "maxItems": 100,
        "maxConcurrency": 10,
        "minConcurrency": 1,
        "maxRequestRetries": 100,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }

    try:
        # Run the Actor and wait for it to finish
        run = client.actor("cAbCkTzBPP0HFO50f").call(run_input=run_input)

        # Fetch Actor results from the run's dataset
        dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        # Write the results to the "reviews" folder
        if dataset_items:
            # Extract the "shortName" from the first review
            short_name = dataset_items[0]["employer"]["shortName"] if "employer" in dataset_items[0] and "shortName" in dataset_items[0]["employer"] else "unknown"
            output_json_path = os.path.join(default_reviews_folder, f"{short_name}_reviews.json")

            # Save to the "reviews" folder
            with open(output_json_path, mode="w", encoding="utf-8") as json_file:
                json.dump(dataset_items, json_file, indent=2, ensure_ascii=False)

            print(f"Results saved to {output_json_path}")
        else:
            print(f"No data found for URL: {url}")
    except Exception as e:
        print(f"An error occurred while processing URL {url}: {e}")
