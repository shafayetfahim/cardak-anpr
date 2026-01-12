import requests
import os

API_URL = "http://127.0.0.1:8000/api/upload/"
IMAGE_PATH = "car.jpg" 

def send_test_image():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Could not find {IMAGE_PATH}. Please place an image in this folder.")
        return

    with open(IMAGE_PATH, 'rb') as img:
        files = {'image': img}
        payload = {'camera_id': 'Front-Gate-01'}
        
        try:
            print(f"Sending {IMAGE_PATH} to {API_URL}...")
            response = requests.post(API_URL, files=files, data=payload)
            
            if response.status_code == 201 or response.status_code == 200:
                print("Success! Image uploaded.")
                print("Server Response:", response.json())
            else:
                print(f"Failed. Status Code: {response.status_code}")
                print("Error Detail:", response.text)
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the server. Is 'python manage.py runserver' running?")

if __name__ == "__main__":
    send_test_image()