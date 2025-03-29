from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
import requests
from db import get_db_connection

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@routes_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user_id = current_user.id
    results = []  # 🔹 Inicjalizacja zmiennej, żeby uniknąć błędu
    search_query = request.form.get('search_query', '')  # Pobieramy poprzednią wartość (lub pusty string)
    selected_inks = request.form.getlist('ink')  # Pobieramy wybrane kolory (lista!)

    # Budujemy URL API dynamicznie
    api_url = "https://api.lorcast.com/v0/cards/search?q="

    filters = []
    if search_query:
        filters.append(search_query)
    if selected_inks:
        ink_filter = " OR ".join(selected_inks)  # API akceptuje wiele kolorów
        filters.append(f"ink:{ink_filter}")

    if filters:
        api_url += " AND ".join(filters)

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])  # 🔹 Jeśli API nie zwróci "results", zwrócimy pustą listę

        for card in results:
            card['in_collection'] = check_if_card_in_collection(user_id, card['id'])
            card['count'] = get_card_count(user_id, card['id'])

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
    except ValueError as e:
        print(f"JSON parsing error: {e}")

    return render_template('search.html', results=results, search_query=search_query, selected_inks=selected_inks)

@routes_bp.route('/add_to_collection/<card_id>')
@login_required
def add_to_collection(card_id):
    user_id = current_user.id
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_collections (user_id, card_id, count) VALUES (%s, %s, 1) "
            "ON DUPLICATE KEY UPDATE count = count + 1",
            (user_id, card_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('routes.search'))

@routes_bp.route('/remove_from_collection/<card_id>')
@login_required
def remove_from_collection(card_id):
    user_id = current_user.id
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_collections WHERE user_id = %s AND card_id = %s", (user_id, card_id))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('routes.search'))

def check_if_card_in_collection(user_id, card_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_collections WHERE user_id = %s AND card_id = %s", (user_id, card_id))
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result > 0
    return False

def get_card_count(user_id, card_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(count) FROM user_collections WHERE user_id = %s AND card_id = %s", (user_id, card_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result and result[0] else 0
    return 0