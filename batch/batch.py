import csv
from datetime import datetime
import requests

# Configuration
CSV_FILE_PATH = "./import-files/workouts.csv"  # Replace with your actual file path
GET_ENDPOINT = "http://127.0.0.1:8000/api/workouts/types"
POST_ENDPOINT = "http://127.0.0.1:8000/api/workouts"

def main():
    # 1. Fetch workout types from the API
    try:
        response = requests.get(GET_ENDPOINT)
        response.raise_for_status()
        workout_types_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return

    # 2. Build a lookup dictionary: {WorkoutName: WorkoutTypeId}
    workout_lookup = {
        item["WorkoutName"]: item["WorkoutTypeId"] 
        for item in workout_types_data
    }

    # 3. Read the CSV file and post the data
    try:
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                workout_name = row["Workout Name"]
                raw_date = row["Workout Date"]
                sequence_str = row["Sequence"]
                
                # Look up the ID based on the name
                workout_id = workout_lookup.get(workout_name)
                
                if workout_id is None:
                    print(f"ERROR: Workout '{workout_name}' not found in the API list. Skipping...")
                    continue  # Move to the next item

                try:
                    # Parse 'M/D/YYYY' from CSV and format to 'YYYY-MM-DD' for the payload
                    formatted_date = datetime.strptime(raw_date, "%m/%d/%Y").strftime("%Y-%m-%d")
                    # Safely convert sequence string to an integer
                    sequence = int(sequence_str)
                except ValueError as e:
                    print(f"ERROR: Skipping '{workout_name}' due to invalid date/sequence format: {e}")
                    continue

                # Construct the payload
                payload = {
                    "WorkoutTypeId": workout_id,
                    "WorkoutDate": formatted_date,
                    "Sequence": sequence
                }

                # 4. POST the payload to the endpoint
                try:
                    post_response = requests.post(POST_ENDPOINT, json=payload)
                    if post_response.ok:
                        print(f"Successfully posted '{workout_name}' (ID: {workout_id})")
                    else:
                        print(f"FAILED to post '{workout_name}': Status {post_response.status_code} - {post_response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Network error trying to post '{workout_name}': {e}")
                    
    except FileNotFoundError:
        print(f"Error: The file at {CSV_FILE_PATH} was not found.")
    except KeyError:
        print("Error: Please check CSV headers. Expected 'Workout Name', 'Workout Date', and 'Sequence'.")

if __name__ == "__main__":
    main()
