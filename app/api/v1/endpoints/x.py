from fastapi import APIRouter, HTTPException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import logging
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/reply", tags=["x-resource"])
def reply(username: str, index: int, reply: str):
    """Reply to a user's tweet by index."""
    from app.main import xdriver as driver
    try:
        driver.get(f"https://x.com/{username}")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//article")))

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

        time.sleep(3)
        return {"message": f"Replied to {username}'s tweet successfully!"}

    except Exception as e:
        logger.error(f"Error in /reply endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/post", tags=["x-resource"])
def post(post: str):
    """Post a tweet."""
    from app.main import xdriver as driver
    try:
        driver.get("https://x.com/compose/tweet")

        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Post text' and @data-testid='tweetTextarea_0']")))

        text_field = driver.find_element(By.XPATH, "//div[@aria-label='Post text' and @data-testid='tweetTextarea_0']")
        text_field.send_keys(post + " ")

        tweet_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@data-testid, 'tweetButton')]")))
        tweet_button.click()

        time.sleep(3)
        return {"message": "Tweet posted successfully!", "tweet_content": post}

    except Exception as e:
        logger.error(f"Error in /post endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user", tags=["x-resource"])
def get_users():
    """Get all users from database."""
    from app.db.session import SessionLocal
    from app.models.users import User
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        logger.error(f"Error in /user endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user", tags=["x-resource"])
def save_user(name: str , username: str, comment_type: str):
    """Save new user in database."""
    from app.db.session import SessionLocal
    from app.models.users import User
    db = SessionLocal()
    try:
        new_user = User(name=name, username=username , created_at=datetime.now(), comment_type=comment_type)
        db.add(new_user)
        db.commit()
        return {"message": "User saved successfully!"}
    except Exception as e:
        logger.error(f"Error in /user endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comment", tags=["x-resource"])
def get_comments(user_id: int = None):
    """Get all comments from database."""
    from app.db.session import SessionLocal
    from app.models.comments import Comment
    db = SessionLocal()
    try:
        if user_id:
            comments = db.query(Comment).filter_by(user_id=user_id).all()
        else:
            comments = db.query(Comment).all()
        return comments
    except Exception as e:
        logger.error(f"Error in /comment endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/comment", tags=["x-resource"])
def save_comment(comment: str, user_id: int):
    """Save new comment in database."""
    from app.db.session import SessionLocal
    from app.models.comments import Comment
    db = SessionLocal()
    try:
        new_comment = Comment(comment=comment, user_id=user_id)
        db.add(new_comment)
        db.commit()
        return {"message": "Comment saved successfully!"}
    except Exception as e:
        logger.error(f"Error in /comment endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))



