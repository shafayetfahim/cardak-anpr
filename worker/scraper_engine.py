from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_vehicle_specs(plate_number):
    options = Options()
    options.add_argument("--headless=new")  # Modern headless mode for speed
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    try:
        # Navigate directly to O'Reilly lookup
        url = f"https://www.oreillyauto.com/lookup?plate={plate_number}"
        driver.get(url)

        # Wait for the vehicle title to appear
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vehicle-name"))
        )

        return element.text  # Returns something like "2018 Honda Civic"
    except Exception as e:
        print(f"Scraper Error: {e}")
        return None
    finally:
        driver.quit()