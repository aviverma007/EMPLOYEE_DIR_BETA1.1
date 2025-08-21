from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def root():
    return jsonify({
        "message": "Frontend-Only Employee Directory API", 
        "status": "running", 
        "mode": "minimal"
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "mode": "frontend-only"})

@app.route('/api/employees')
def get_employees():
    return jsonify({
        "message": "Data is now managed by frontend", 
        "redirect": "Use frontend dataService"
    })

@app.route('/api/departments')
def get_departments():
    return jsonify({
        "message": "Data is now managed by frontend", 
        "redirect": "Use frontend dataService"
    })

@app.route('/api/locations')
def get_locations():
    return jsonify({
        "message": "Data is now managed by frontend", 
        "redirect": "Use frontend dataService"
    })

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "message": "Data is now managed by frontend", 
        "redirect": "Use frontend dataService"
    })

@app.route('/api/meeting-rooms')
def get_meeting_rooms():
    return jsonify({
        "message": "Meeting rooms API is now handled by frontend dataService", 
        "redirect": "Use frontend dataService"
    })

@app.route('/api/meeting-rooms/<room_id>/book', methods=['POST'])
def book_meeting_room(room_id):
    return jsonify({
        "message": f"Meeting room booking for {room_id} is now handled by frontend dataService", 
        "redirect": "Use frontend dataService"
    })

# Catch-all for other API endpoints
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all_api(path):
    return jsonify({
        "message": f"API endpoint /{path} is now handled by frontend dataService",
        "mode": "frontend-only",
        "redirect": "Use frontend dataService"
    })

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)