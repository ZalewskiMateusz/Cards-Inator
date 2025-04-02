from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from db import get_db_connection


events_bp = Blueprint('events', __name__)

@events_bp.route('/event/new', methods=['POST'])
@login_required
def create_event():
    data = request.json

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO events (name, date, image_url, description, is_public, is_recurring, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        cursor.execute(query, (
            data['name'],
            data['date'],  # Data w formacie YYYY-MM-DD HH:MM:SS
            data.get('image_url', ''),
            data['description'],
            data.get('is_public', True),
            data.get('is_recurring', False),
            current_user.id
        ))

        conn.commit()
        event_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Event created successfully!", "event_id": event_id}), 201


    except Exception as e:
        return jsonify({"error": str(e)}), 500