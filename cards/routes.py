# cards/routes.py
from flask import Blueprint, jsonify
from database import get_connection
from flask import request

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/cards')
def get_cards():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, img FROM cards")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    cards = [{'id': r[0], 'name': r[1], 'img': r[2]} for r in rows]
    return jsonify(cards)

@cards_bp.route('/cards/<int:card_id>', methods=['GET'])
def get_card_by_id(card_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, subtitle, energy, might, power, abilities,
               flavor, img
        FROM cards
        WHERE id = %s
    """, (card_id,))
    
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        card = {
            'id': row[0],
            'name': row[1],
            'subtitle': row[2],
            'energy': row[3],
            'might': row[4],
            'power': row[5],
            'abilities': row[6],
            'flavor': row[7],
            'img': row[8],
        }
        return jsonify(card)
    else:
        return jsonify({'error': 'Carta não encontrada'}), 404

#Rota regions
@cards_bp.route('/regions')
def get_regions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM region ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    regions = [{'id': r[0], 'name': r[1]} for r in rows]
    return jsonify(regions)

#Rota keywords
@cards_bp.route('/keywords')
def get_keywords():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM keywords ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

#runes
@cards_bp.route('/runes')
def get_runes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM runes ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

#champion
@cards_bp.route('/champions')
def get_champion():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM champion ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

#kind
@cards_bp.route('/kinds')
def get_kind():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM kind ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

#type
@cards_bp.route('/types')
def get_type():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM type ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

#rarity
@cards_bp.route('/rarities')
def get_rarity():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM rarity ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{'id': r[0], 'name': r[1]} for r in rows])

#filtro cartas
@cards_bp.route('/cards')
def get_cards():
    conn = get_connection()
    cur = conn.cursor()

    region = request.args.get('region')
    keyword = request.args.get('keyword')

    query = """
        SELECT c.id, c.name, c.img
        FROM cards c
        LEFT JOIN card_region cr ON c.id = cr.card_id
        LEFT JOIN region r ON r.id = cr.region_id
        LEFT JOIN card_keywords ck ON c.id = ck.card_id
        LEFT JOIN keywords k ON k.id = ck.keyword_id
        WHERE 1=1
    """

    params = []

    if region:
        query += " AND r.name = %s"
        params.append(region)

    if keyword:
        query += " AND k.name = %s"
        params.append(keyword)

    query += " GROUP BY c.id ORDER BY c.name"

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    cards = [{'id': r[0], 'name': r[1], 'img': r[2]} for r in rows]
    return jsonify(cards)
