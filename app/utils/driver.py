import undetected_chromedriver as uc
import logging
import pickle
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

active_drivers = {}

def setup_driver(session_id: str):
    """Set up and return an undetected ChromeDriver."""
    options = uc.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options)
    active_drivers[session_id] = driver
    logger.info("WebDriver created for session ID: %s", session_id)
    return driver

def load_cookies(driver, cookie_file="cookies/x_cookies.pkl"):
    """Load saved cookies into Selenium or save new cookies if they don't exist."""
    os.makedirs(os.path.dirname(cookie_file), exist_ok=True)

    if os.path.exists(cookie_file):
        try:
            driver.get("https://x.com")
            time.sleep(3)
            cookies = pickle.load(open(cookie_file, "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(3)
            logger.info("Cookies loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
    else:
        logger.info("No cookies found. Please log in to save cookies.")
        driver.get("https://x.com/login")
        input("Press Enter after logging in...")
        pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
        logger.info("Cookies saved successfully.")

def close_driver(session_id: str):
    """Close the WebDriver for a specific session."""
    driver = active_drivers.pop(session_id, None)
    if driver:
        driver.quit()
        logger.info("WebDriver closed for session ID: %s", session_id)
