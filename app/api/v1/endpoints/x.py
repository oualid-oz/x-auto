from fastapi import APIRouter, HTTPException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

from app.utils.driver import setup_driver, load_cookies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/reply", tags=["x-resource"])
def reply(username: str, index: int, reply: str, session_id: str = "session_1"):
    """Reply to a user's tweet by index."""
    global driver
    try:
        driver = setup_driver(session_id)
        load_cookies(driver)
        driver.get(f"https://x.com/{username}")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//article")))

        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)

        tweets = driver.find_elements(By.XPATH, "//article")
        if index >= len(tweets):
            raise HTTPException(status_code=400, detail="Tweet index out of range")

        tweet = tweets[index]

        reply_button = None
        possible_xpaths = [
            ".//div[@role='button' and contains(@data-testid, 'reply')]",
            ".//button[contains(@data-testid, 'reply')]",
        ]

        for xpath in possible_xpaths:
            try:
                reply_button = tweet.find_element(By.XPATH, xpath)
                break
            except:
                continue

        if not reply_button:
            raise HTTPException(status_code=404, detail="Reply button not found")

        reply_button.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='textbox' and @data-testid='tweetTextarea_0']")))
        text_field = driver.find_element(By.XPATH, "//div[@role='textbox' and @data-testid='tweetTextarea_0']")
        
        text_field.send_keys(reply+" ")

        tweet_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@data-testid, 'tweetButton')]")))
        tweet_button.click()

        driver.quit()
        time.sleep(3)
        return {"message": f"Replied to {username}'s tweet successfully!"}

    except Exception as e:
        logger.error(f"Error in /reply endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))