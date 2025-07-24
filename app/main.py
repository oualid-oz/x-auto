from fastapi import FastAPI
from app.api.v1.endpoints import x
from app.db.session import engine, Base
from app.utils.driver import setup_driver, load_cookies
from pyfiglet import figlet_format
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup_banner():
    # Font: doom, slant, jazmine, big_money-nw, standard, drpepper, jacky
    #       fire_font-s, banner3-D, ansi_regular, epic, stop, larry3d
    #       ansi_shadow, speed, colossal
    print(figlet_format("X Replyer", font="slant"))

xdriver = setup_driver("X session")
load_cookies(xdriver)

Base.metadata.create_all(bind=engine)

app.include_router(x.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001 , reload=True)
