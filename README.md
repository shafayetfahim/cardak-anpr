Cardak, an Event-Driven Vehicle Indexer (ANPR)

In New York State, there are registration stickers on windshields that diagnose what a car's year, make, and model is. What if you could take it one step further and get all of this information
from simply the license plate?

Cardak is an automated license plate recognition pipeline built with Django, Redis, and PyTorch. It uses an event-driven architecture to ingest images via an API, 
process them asynchronously using EasyOCR, and enrich the data by scraping external vehicle databases. 

Here's some features I implemented:

- Asynchronous Task Offloading:
Instead of making the user wait for the image to process, the Django API instantly accepts the upload and offloads the heavy lifting to a Redis queue. This keeps the web server responsive even under high load.

- Optical Character Recognition (OCR):
Using the EasyOCR library (powered by PyTorch), the system identifies text regions in an image and extracts alphanumeric characters to determine the license plate number.

- Automated Data Enrichment:
Once a plate is read, the worker doesn't stop there. It queries external APIs (like NHTSA) or scrapes data sources to convert a simple string like "JLM7605" into a full vehicle profile (e.g., "2015 Honda Civic").

- Reliable Queue Management:
Built on top of my "SentinelQueue" architecture, the system ensures that if the OCR worker crashes while processing an image, the task is rescued and retried rather than being lost.

- Containerized Infrastructure:
The database (PostgreSQL) and message broker (Redis) run in Docker containers, ensuring the environment is consistent and easy to spin up on any machine.

Here's the internal structure:

* indexer/: The Django application handling the REST API endpoints and database models.
* worker/: The background engine that performs the OCR, scrapes vehicle data, and updates the database.
* sentinel_client/: My custom reliability layer that handles atomic queue operations and task safety.
* core/: The main Django configuration and settings.

To run this...

1. Start the infrastructure: docker-compose up -d
2. Launch the Web Server: python manage.py runserver
3. Start the Worker: python worker/main.py
4. Simulate a Camera: python worker/simulate_camera.py

In the future, I'd like to fix the missing link between license plate and VIN using clever headless browsers that use external providers, and perhaps implement all of this onto RaspberryOS and peripherals.
