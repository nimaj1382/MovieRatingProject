from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException


from app.api.v1 import api_router
from app.db.base import Base
from app.db.session import engine
from app.utils.logging_config import logger


# Initialize logging
logger.info("Initializing Movie Rating API...")


# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Movie Rating API",
    description="A simple Movie Rating API built with FastAPI.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

logger.info("Movie Rating API initialized successfully")

app.exception_handlers = {}


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failure",
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": "failure",
            "error": {
                "code": 422,
                "message": str(exc.errors())
            }
        }
    )


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(
    api_router,
    prefix="/api/v1",
)

@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Movie Rating API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)