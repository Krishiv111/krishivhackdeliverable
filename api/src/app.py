from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncIterator

from fastapi import FastAPI, Form, status,  APIRouter
from fastapi.responses import RedirectResponse
from typing_extensions import TypedDict
from datetime import datetime, timedelta

from services.database import JSONDatabase


class Quote(TypedDict):
    name: str
    message: str
    time: str


database: JSONDatabase[list[Quote]] = JSONDatabase("data/database.json")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle database management when running app."""
    if "quotes" not in database: 
        print("Adding quotes entry to database")
        database["quotes"] = []

    yield

    database.close()


app = FastAPI(lifespan=lifespan)


router = APIRouter(prefix="/api")

@router.post("/quote")
def post_message(name: str = Form(), message: str = Form()) -> RedirectResponse:
    """
    Process a user submitting a new quote.
    You should not modify this function except for the return value.
    """
    now = datetime.now()
    quote = Quote(name=name, message=message, time=now.isoformat(timespec="seconds"))
    database["quotes"].append(quote)

    # You may modify the return value as needed to support other functionality
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

@router.get("/quotes") # Get the quotes this is Part of CRUD which get the quotes when typing in the /quotes
def get_quotes():
    return database["quotes"]


# TODO: add another API route with a query parameter to retrieve quotes based on max age
# I learned a lot and how to specifically do this correctly and work with query parameters through Zeq Tech Youtube Videos on FAST API

@router.get("/quotes/filter")
async def get_quotes_by_age(max_age: int):
    
    cutoff = datetime.now() - timedelta(minutes=max_age)

    filtered = [
        quote for quote in database["quotes"]
        if datetime.fromisoformat(quote["time"]) >= cutoff
    ]

    return filtered

app.include_router(router)