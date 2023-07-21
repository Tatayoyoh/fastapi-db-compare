from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api.core as core
import api.test1 as test1
import api.test2 as test2
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

# Routes
app.include_router(core.router)

