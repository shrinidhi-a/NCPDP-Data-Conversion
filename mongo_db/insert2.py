import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["healthcare"]
collection = db["sampleData"]

json_filepath = 'output/sample2.json'

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # If data is a list, use it directly
    documents = data if isinstance(data, list) else list(data.values())

    if documents:
        collection.insert_many(documents)
        print(f"✅ Inserted {len(documents)} documents into MongoDB.")
    else:
        print("No data found to insert.")

except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")

client.close()
