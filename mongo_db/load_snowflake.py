#Script to connect python and Snowflake
import snowflake.connector
import pandas as pd

try:
    # Connect to Snowflake
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

    # Load data
    final_df = pd.read_csv("csv/MTMData.csv")

    # Rename columns to match Snowflake table exactly
    final_df.rename(columns={
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
    }, inplace=True)

    # Ensure all required columns exist
    expected_columns = [
        'RECORD_TYPE', 'TRANSACTION_ID', 'DATE', 'PHARMACY_NCPDP_ID', 'PHARMACIST_NPI',
        'PATIENT_ID', 'PATIENT_NAME', 'DOB', 'GENDER', 'PAYER_ID', 'PLAN_NAME',
        'INTERVENTION_TYPE', 'MTM_SERVICE_CODE', 'START_DATE', 'END_DATE',
        'OUTCOME', 'RECOMMENDATIONS', 'PRESCRIBER_CONTACTED', 'PRESCRIBER_NPI',
        'PRESCRIBER_RESPONSE', 'FOLLOW_UP_DATE', 'NOTES'
    ]
    missing_cols = [col for col in expected_columns if col not in final_df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in CSV: {missing_cols}")

    # Insert rows
    insert_query = f"""
        INSERT INTO MTM_RECORDS ({', '.join(expected_columns)})
        VALUES ({', '.join(['%s'] * len(expected_columns))})
    """
    for _, row in final_df.iterrows():
        values = tuple(row.fillna("").values.tolist())
        cursor.execute(insert_query, values)

    conn.commit()
    print("Data uploaded successfully to MTM_RECORDS table.")


except Exception as e:
    print(f"Error: {e}")

finally:
    try:
        cursor.close()
        conn.close()
    except:
        pass
