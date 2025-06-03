import pandas as pd
from pymongo import MongoClient
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

try:
    # Step 1: Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', "mongodb://localhost:27017") #Get MongoDB URL from environment or default to localhost
    mongo_client = MongoClient(mongo_url)
    db = mongo_client["healthcare"]
    collection = db["sampleData"]

    # Step 2: Load data from MongoDB
    documents = list(collection.find())
    if not documents:
        raise ValueError("No documents found in MongoDB collection.")

    # Step 3: Convert to DataFrame
    df = pd.DataFrame(documents)

    # Step 4: Drop MongoDB internal _id field
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # Expected columns in uppercase with underscores
    expected_columns = [
        "RECORD_TYPE", "TRANSACTION_ID", "DATE", "PHARMACY_NCPDP_ID", "PHARMACIST_NPI",
        "PATIENT_ID", "PATIENT_NAME", "DOB", "GENDER", "PAYER_ID", "PLAN_NAME",
        "INTERVENTION_TYPE", "MTM_SERVICE_CODE", "START_DATE", "END_DATE", "OUTCOME",
        "RECOMMENDATIONS", "PRESCRIBER_CONTACTED", "PRESCRIBER_NPI", "PRESCRIBER_RESPONSE",
        "FOLLOW_UP_DATE", "NOTES"
    ]

    # Rename columns
    rename_map = {
        "Record Type": "RECORD_TYPE",
        "Transaction ID": "TRANSACTION_ID",
        "Date": "DATE",
        "Pharmacy NCPDP ID": "PHARMACY_NCPDP_ID",
        "Pharmacist NPI": "PHARMACIST_NPI",
        "Patient ID": "PATIENT_ID",
        "Patient Name": "PATIENT_NAME",
        "DOB": "DOB",
        "Gender": "GENDER",
        "Payer ID": "PAYER_ID",
        "Plan Name": "PLAN_NAME",
        "Intervention Type": "INTERVENTION_TYPE",
        "MTM Service Code": "MTM_SERVICE_CODE",
        "Start Date": "START_DATE",
        "End Date": "END_DATE",
        "Outcome": "OUTCOME",
        "Recommendations": "RECOMMENDATIONS",
        "Prescriber Contacted": "PRESCRIBER_CONTACTED",
        "Prescriber NPI": "PRESCRIBER_NPI",
        "Prescriber Response": "PRESCRIBER_RESPONSE",
        "Follow-up Date": "FOLLOW_UP_DATE",
        "Notes": "NOTES"
    }
    df.rename(columns=rename_map, inplace=True)

    # Filter dataframe to keep only expected columns present in df
    df = df[[col for col in expected_columns if col in df.columns]]

    # Convert datetime columns to string
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)

    # Convert dict/list columns to string without deprecated applymap
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, (dict, list)) else x)

    # Step 7: Connect to Snowflake
    conn = snowflake.connector.connect(
    user=os.environ.get('SNOWFLAKE_USER'),
    password=os.environ.get('SNOWFLAKE_PASSWORD'),
    account=os.environ.get('SNOWFLAKE_ACCOUNT'),
    warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
    database=os.environ.get('SNOWFLAKE_DATABASE'),
    schema=os.environ.get('SNOWFLAKE_SCHEMA'),
    role=os.environ.get('SNOWFLAKE_ROLE')
    )
    cursor = conn.cursor()

    # Step 8: Prepare Insert Query with quoted column names
    table_name = 'MTMFormattedData'
    columns = list(df.columns)
    quoted_columns = ', '.join([f'"{col}"' for col in columns])
    placeholders = ', '.join(['%s'] * len(columns))

    insert_query = f"""
        INSERT INTO {table_name} ({quoted_columns})
        VALUES ({placeholders})
    """

    # Step 9: Insert data row by row
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
