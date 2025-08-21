from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="Frontend-Only Employee Directory API", version="1.0.0")

# CORS middleware - allow all origins for frontend-only mode
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Frontend-Only Employee Directory API", "status": "running", "mode": "minimal"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "frontend-only"}

# Minimal API endpoints for compatibility (all return empty responses)
@app.get("/api/employees")
async def get_employees():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

@app.get("/api/departments")
async def get_departments():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

@app.get("/api/locations")
async def get_locations():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

@app.get("/api/stats")
async def get_stats():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

# Catch-all for other API endpoints
@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all_api(path: str):
    return JSONResponse(
        status_code=200,
        content={
            "message": f"API endpoint /{path} is now handled by frontend dataService",
            "mode": "frontend-only",
            "redirect": "Use frontend Excel parsing"
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)