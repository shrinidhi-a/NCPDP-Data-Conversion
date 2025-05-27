import pandas as pd
import snowflake.connector

try:
    # Snowflake connection
    conn = snowflake.connector.connect(
        user='Fizan',
        password='Fizanshareef998800',
        account='BU51577',
        warehouse='SNOWFLAKE_LEARNING_WH',
        database='SNOWFLAKE_LEARNING_DB',
        schema='pharmacist'
    )
    cursor = conn.cursor()

    # Test connection
    cursor.execute("SELECT CURRENT_USER()")
    user = cursor.fetchone()
    print(f"Connected to Snowflake as user: {user[0]}")

except snowflake.connector.errors.Error as e:
    print("Connection to Snowflake failed:", e)
    exit()

# If connected, proceed with the rest
csv_files = ['patients.csv', 'careplans.csv', 'providers.csv', 'allergies.csv',
             'procedures.csv', 'observations.csv', 'medications.csv', 'payers.csv',
             'supplies.csv', 'conditions.csv', 'devices.csv', 'encounters.csv',
             'imaging_studies.csv', 'immunizations.csv', 'organizations.csv',
             'payer_transitions.csv']

# for file in csv_files:
#     df = pd.read_csv(file)

#     for index, row in df.iterrows():
#         # Replace with actual table and column names
#         cursor.execute("""
#             INSERT INTO your_table (col1, col2, col3)
#             VALUES (%s, %s, %s)
#         """, (row['col1'], row['col2'], row['col3']))

conn.commit()
cursor.close()
conn.close()
