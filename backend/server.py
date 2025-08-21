from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Frontend-Only Employee Directory API", "status": "running", "mode": "minimal"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "frontend-only"}

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

@app.get("/api/meeting-rooms")
async def get_meeting_rooms():
    return {"message": "Meeting rooms API is now handled by frontend dataService", "redirect": "Use frontend dataService"}

@app.post("/api/meeting-rooms/{room_id}/book")
async def book_meeting_room(room_id: str):
    return {"message": f"Meeting room booking for {room_id} is now handled by frontend dataService", "redirect": "Use frontend dataService"}

# Catch-all for other endpoints
@app.api_route("/api/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(full_path: str, request: Request):
    return {
        "message": f"API endpoint /{full_path} is now handled by frontend dataService",
        "mode": "frontend-only",
        "redirect": "Use frontend dataService"
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)