import csv
import json
import os

def csv_to_json_nested(csv_dir, json_filepath, limit=50):
    files = [
        'patients.csv', 'careplans.csv', 'providers.csv', 'allergies.csv',
        'procedures.csv', 'observations.csv', 'medications.csv', 'payers.csv',
        'supplies.csv', 'conditions.csv', 'devices.csv', 'encounters.csv',
        'imaging_studies.csv', 'immunizations.csv', 'organizations.csv',
        'payer_transitions.csv'
    ]

    patient_data = {}

    # Step 1: Load patients.csv
    try:
        with open(os.path.join(csv_dir, 'patients.csv'), 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                pid = row.get('Id')
                if pid:
                    patient_data[pid] = {'patient_details': row}
    except Exception as e:
        print(f"Error loading patients.csv: {e}")
        return

    # Step 2: Load all other files and group by PATIENT ID
    for file in files[1:]:
        path = os.path.join(csv_dir, file)
        key = file.replace('.csv', '')

        try:
            with open(path, 'r', encoding='utf-8') as f:
                for i, row in enumerate(csv.DictReader(f)):
                    if i >= limit:
                        break
                    pid = row.get('PATIENT')
                    if pid in patient_data:
                        patient_data[pid].setdefault(key, []).append(row)
        except FileNotFoundError:
            print(f"Missing file: {file}, skipping...")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    # Step 3: Save to JSON
    try:
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(patient_data, f, indent=4)
        print(f"✅ Data saved to {json_filepath}")
    except Exception as e:
        print(f"Error writing JSON: {e}")

# Example usage
csv_dir = 'csv'
json_filepath = 'sampleOutput.json'
csv_to_json_nested(csv_dir, json_filepath)
