import requests
import json
import redis
import psycopg2
import time
from ocr_engine import extract_plate

# Initialize Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)


def update_db(asset_id, plate, specs):
    """Saves the final results to PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname="cardak_db", user="user", password="password", host="db"
        )
        cur = conn.cursor()
        cur.execute("""
            UPDATE indexer_vehicleasset 
            SET license_plate = %s, model = %s, status = 'COMPLETED'
            WHERE id = %s
        """, (plate, specs, asset_id))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully updated database for Asset ID: {asset_id}")
    except Exception as e:
        print(f"Database update failed: {e}")


def get_nhtsa_data(vin):
    """Enriches the data using the free NHTSA API."""
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    try:
        response = requests.get(url, timeout=10)
        data = {item['Variable']: item['Value'] for item in response.json().get('Results', []) if item['Value']}
        return f"{data.get('Model Year', '')} {data.get('Make', '')} {data.get('Model', '')}".strip()
    except Exception as e:
        print(f"API Error: {e}")
        return "Unknown Vehicle"


def main():
    print("Worker started. Listening for tasks...")
    while True:
        try:
            result = r.brpop("ocr_tasks", timeout=0)
            if not result: continue
            _, message = result
            task = json.loads(message)

            # Step 1: AI OCR
            plate = extract_plate(task['image_path'])
            if plate:
                # Step 2: API Enrichment
                specs = get_nhtsa_data("5YJ3E1EB8JF")
                # Step 3: Persist
                update_db(task['asset_id'], plate, specs)
        except Exception as e:
            print(f"Worker Loop Error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()