# python -m venv venv
# venv/bin/activate

# uvicorn app.main:app --reload
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import itinerary_router, recommendation_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Itinerary API",
    description="API for managing travel itineraries",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(itinerary_router)
app.include_router(recommendation_router)

@app.get("/")
def root():
    return {"message": "Travel Itinerary API is running"}

@app.get("/api")
def api_info():
    return {
        "message": "Welcome to the Travel Itinerary API",
        "endpoints": {
            "itineraries": {
                "get": "/api/itineraries - Get all itineraries with optional filtering",
                "getById": "/api/itineraries/{id} - Get a specific itinerary by ID",
                "post": "/api/itineraries - Create a new itinerary",
                "put": "/api/itineraries/{id} - Update an existing itinerary",
                "delete": "/api/itineraries/{id} - Delete an itinerary"
            },
            "recommendations": {
                "get": "/api/recommendations?nights=3 - Get recommended itineraries for given nights",
                "popular": "/api/recommendations/popular - Get popular itineraries",
                "stats": "/api/recommendations/stats - Get itinerary statistics"
            }
        }
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "error": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)