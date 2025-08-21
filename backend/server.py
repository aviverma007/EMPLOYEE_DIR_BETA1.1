from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Frontend-Only Employee Directory API", "status": "running", "mode": "minimal"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "mode": "frontend-only"}

@app.get("/api/employees")
def get_employees():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

@app.get("/api/departments")
def get_departments():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

@app.get("/api/locations")
def get_locations():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

@app.get("/api/stats")
def get_stats():
    return {"message": "Data is now managed by frontend", "redirect": "Use frontend dataService"}

@app.get("/api/meeting-rooms")
def get_meeting_rooms():
    return {"message": "Meeting rooms API is now handled by frontend dataService", "redirect": "Use frontend dataService"}

@app.post("/api/meeting-rooms/{room_id}/book")
def book_meeting_room(room_id: str):
    return {"message": f"Meeting room booking for {room_id} is now handled by frontend dataService", "redirect": "Use frontend dataService"}

@app.get("/api/{path:path}")
def catch_all_get(path: str):
    return {"message": f"API endpoint /{path} is now handled by frontend dataService", "mode": "frontend-only", "redirect": "Use frontend dataService"}

@app.post("/api/{path:path}")
def catch_all_post(path: str):
    return {"message": f"API endpoint /{path} is now handled by frontend dataService", "mode": "frontend-only", "redirect": "Use frontend dataService"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)