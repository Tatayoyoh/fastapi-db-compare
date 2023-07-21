from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api.core as core
import api.test1 as test1
import api.test2 as test2
import api.test3 as test3
from settings import settings
from utils.response import ServerError, NotFound, Error, DEFAULT_RESPONSES

app = FastAPI(responses=DEFAULT_RESPONSES)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_allow_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception auto handle
@app.exception_handler(Exception)
async def validation_exception_handler(request, e):
    return ServerError(str(e))

# @app.exception_handler(DatabaseException)
async def validation_exception_handler(request, e):
    return Error(str(e))

# @app.exception_handler(DatabaseNotFoundError)
async def validation_exception_handler(request, e):
    return NotFound(str(e))


# Routes
app.include_router(core.router)
app.include_router(test1.router)
app.include_router(test2.router)
app.include_router(test3.router)
# Database

from utils.db import database, metadata, DB_URL
app.state.database = database
import sqlalchemy
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from utils.db import MONGO_URL
from api.test3 import StudentFriendBeanie, ParentBeanie, AddressBeanie, SchoolBeanie, StudentBeanie

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        engine = sqlalchemy.create_engine(DB_URL)
        metadata.create_all(engine)

    """ Beanie Initialize application services"""
    app.db = AsyncIOMotorClient(MONGO_URL).example_db
    await init_beanie(app.db, document_models=[StudentFriendBeanie, ParentBeanie, AddressBeanie, SchoolBeanie, StudentBeanie])


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


