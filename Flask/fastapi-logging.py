
# logging_config.py

import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}

logging.config.dictConfig(LOGGING_CONFIG)


# main.py

from fastapi import FastAPI
import logging
from logging_config import LOGGING_CONFIG

app = FastAPI()

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("my_logger")

@app.get("/")
async def root():
    # Log an info message
    logger.info("Received a request to the root endpoint.")
    return {"message": "Hello, World!"}


# main.py

from fastapi import FastAPI
import logging
from logging_config import LOGGING_CONFIG
from routers import example_router

app = FastAPI()

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("my_logger")

# Include the router
app.include_router(example_router.router)




# routers/example_router.py

from fastapi import APIRouter
import logging

router = APIRouter()

@router.get("/example")
async def example_route():
    # Access the logger defined in main.py
    logger = logging.getLogger("my_logger")

    # Log an info message specific to this route
    logger.info("Received a request to the example route.")

    return {"message": "This is an example route."}
