import requests, json, redis, psycopg2, time, os
from ocr_engine import extract_plate
from scraper_engine import get_vehicle_specs
from dotenv import load_dotenv

load_dotenv()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def update_db(asset_id, plate, specs):
    try:
        conn = psycopg2.connect(dbname="cardak_db", user="user", password="password", host="localhost")
        cur = conn.cursor()
        cur.execute("UPDATE indexer_vehicleasset SET license_plate = %s, model = %s, status = 'COMPLETED' WHERE id = %s", (plate, specs, asset_id))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

def get_nhtsa_data(vin):
    if not vin: return None
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    try:
        res = requests.get(url, timeout=10).json()
        d = {i['Variable']: i['Value'] for i in res.get('Results', []) if i['Value']}
        return f"{d.get('Model Year', '')} {d.get('Make', '')} {d.get('Model', '')}".strip()
    except:
        return None

def main():
    print("Worker started. Listening for tasks...", flush=True)
    while True:
        res = r.brpop("ocr_tasks", timeout=0)
        if not res: continue
        task = json.loads(res[1])
        plate = extract_plate(task['image_path'])
        
        if plate:
            specs = get_vehicle_specs(plate)
            
            if not specs:
                surrogate = os.getenv("SURROGATE_VIN")
                specs = get_nhtsa_data(surrogate)
            
            update_db(task['asset_id'], plate, specs or "Unknown Vehicle")

if __name__ == "__main__":
    main()