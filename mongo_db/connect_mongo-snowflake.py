#Connect MongoDb and snowflake to load the data
import pandas as pd
from pymongo import MongoClient
import snowflake.connector

try:
    # Step 1: Connect to MongoDB
    mongo_client = MongoClient("mongodb://localhost:27017")  # Update if using Atlas
    db = mongo_client["healthcare"] 
    collection = db["patients_data"]

    # Step 2: Load data from MongoDB
    documents = list(collection.find())
    if not documents:
        raise ValueError("No documents found in MongoDB collection.")

    # Step 3: Convert to DataFrame
    df = pd.DataFrame(documents)

    # Step 4: Drop MongoDB internal _id field
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # Step 5: Convert datetime and nested dict/list columns to string
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)

    df = df.applymap(lambda x: str(x) if isinstance(x, (dict, list)) else x)

    # Step 6: Connect to Snowflake
    conn = snowflake.connector.connect(
        user='Fizan',
        password='Tietoevry12345',
        account='bu51577.central-india.azure',
        warehouse='SNOWFLAKE_LEARNING_WH',
        database='SNOWFLAKE_LEARNING_DB',
        schema='MTM_ANALYTICS',
        role='ACCOUNTADMIN'
    )
    cursor = conn.cursor()

    # Step 7: Prepare Insert Query
    table_name = 'MTM_RECORDS'
    columns = list(df.columns)
    insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({', '.join(['%s'] * len(columns))})
    """

    # Step 8: Insert Data
    for _, row in df.iterrows():
        values = tuple(row.fillna("").values.tolist())
        cursor.execute(insert_query, values)

    conn.commit()
    print("✅ JSON data from MongoDB loaded into Snowflake.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    try:
        cursor.close()
        conn.close()
    except:
        pass
