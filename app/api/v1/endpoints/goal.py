from fastapi import APIRouter, HTTPException
from selenium.webdriver.support.ui import WebDriverWait
from pydantic import BaseModel
from app.utils.driver import setup_driver
import logging
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class MatchResult(BaseModel):
    league: str = ""
    home_team: str
    away_team: str
    home_score: str
    away_score: str
    match_status: str
    match_time: str

@router.get("/goal", response_model=list[MatchResult] , tags=["goal-resource"])
async def get_live_matches(url: str):
    driver = None
    try:
        driver = setup_driver()
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        matches = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//section[contains(@class, 'section-with-dividers') and contains(@class, 'match-info_section')]")))
        logger.info(f"Found {len(matches)} matches")

        live_matches = []
        for match in matches:
            try:
                home_team_elem = match.find_element(By.XPATH, ".//a[contains(@class, 'team_team-a')]//span[contains(@class, 'team_team-name')]")
                away_team_elem = match.find_element(By.XPATH, ".//a[contains(@class, 'team_team-b')]//span[contains(@class, 'team_team-name')]")
                
                home_team = home_team_elem.text.strip()
                away_team = away_team_elem.text.strip()

                try:
                    score_elem = match.find_element(By.XPATH, ".//span[contains(@class, 'match-data_score')]")
                    scores = re.findall(r'\d+', score_elem.text)
                    home_score = scores[0] if len(scores) > 0 else "0"
                    away_score = scores[1] if len(scores) > 1 else "0"
                except Exception as score_error:
                    logger.warning(f"Could not extract score: {score_error}")
                    home_score, away_score = "0", "0"

                try:
                    match_status_elem = match.find_element(By.XPATH, ".//span[contains(@class, 'match-period')]")
                    match_status = match_status_elem.text.strip()
                except Exception as status_error:
                    logger.warning(f"Could not extract match status: {status_error}")
                    match_status = "Unknown"

                live_matches.append(MatchResult(
                    home_team=home_team,
                    away_team=away_team,
                    home_score=home_score,
                    away_score=away_score,
                    match_status=match_status,
                    match_time=match_status  # Adjust this if match time is different
                ))
            except Exception as match_error:
                logger.warning(f"Error parsing match: {match_error}")

        return live_matches

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching live matches: {str(e)}")
    finally:
        if driver:
            driver.quit()