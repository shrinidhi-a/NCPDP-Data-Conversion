import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Step 1: Connect to MongoDB
mongo_url = os.environ.get('MONGO_URL', "mongodb://localhost:27017") #Get MongoDB URL from environment or default to localhost
client = MongoClient(mongo_url)
db = client["healthcare"]  
collection = db["patients_data"]  

# Step 2: Load the JSON file you created
json_filepath = 'output/sample.json'

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Step 3: Insert each patient document into MongoDB
    documents = list(data.values())  # Convert dict of patient_id: data to list of documents
    if documents:
        collection.insert_many(documents)
        print(f"✅ Inserted {len(documents)} documents into MongoDB.")
    else:
        print("No data found to insert.")

except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")

# Step 4: Close the connection
client.close()
