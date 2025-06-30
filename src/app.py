# Ficheiro: src/app.py (O ÚNICO FICHEIRO PYTHON QUE PRECISA)

import os
import psycopg2 # Importação do driver da base de dados
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# --- LÓGICA DA BASE DE DADOS (do antigo database.py) ---
def get_connection():
    return psycopg2.connect(
        dbname="riftcards",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )

# --- CONFIGURAÇÃO DA APLICAÇÃO FLASK ---
project_root = Path(__file__).resolve().parent.parent
static_folder_path = project_root / "static"
template_folder_path = project_root / "templates"

app = Flask(
    __name__,
    template_folder=template_folder_path,
    static_folder=static_folder_path
)
CORS(app)

# --- ROTAS DAS PÁGINAS HTML ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cartas.html')
def cartas_page():
    return render_template('cartas.html')

@app.route('/detalhe-carta.html')
def detalhe_carta_page():
    return render_template('detalhe-carta.html')

@app.route('/deck-builder.html')
def deck_builder_page():
    return render_template('deck-builder.html')

@app.route('/meta.html')
def meta_page():
    return render_template('meta.html')


# --- ROTAS DA API (do antigo cards/routes.py) ---
# Adicionámos o prefixo /api aqui diretamente
@app.route('/api/cards')
def get_cards():
    conn = get_connection()
    cur = conn.cursor()

    rarities = request.args.get('rarities', '').split(',') if request.args.get('rarities') else []
    keywords = request.args.get('keywords', '').split(',') if request.args.get('keywords') else []
    max_energy = request.args.get('max_energy', None, type=int)

    params = []
    # --- INÍCIO DA VERSÃO FINAL E CORRETA DA QUERY ---
    query = """
        SELECT DISTINCT c.id, c.name, c.img
        FROM cards c
        LEFT JOIN card_rarity cr ON c.id = cr.card_id      -- Ligação 1: cards -> card_rarity (usando card_id)
        LEFT JOIN rarity r ON cr.rarity_id = r.id          -- Ligação 2: card_rarity -> rarity (usando rarity_id)
        LEFT JOIN card_keywords ck ON c.id = ck.card_id
        LEFT JOIN keywords k ON ck.keyword_id = k.id
        WHERE 1=1
    """
    # --- FIM DA VERSÃO FINAL ---

    if max_energy is not None:
        query += " AND c.energy <= %s"
        params.append(max_energy)

    # O filtro de raridade está agora reativado com a lógica correta
    if rarities:
        query += " AND r.name = ANY(%s)"
        params.append(rarities)

    if keywords:
        query += """
            AND c.id IN (
                SELECT card_id FROM card_keywords cki
                JOIN keywords ki ON cki.keyword_id = ki.id
                WHERE ki.name = ANY(%s)
                GROUP BY card_id
                HAVING COUNT(DISTINCT ki.name) = %s
            )
        """
        params.append(keywords)
        params.append(len(keywords))

    query += " ORDER BY c.name"
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    cards = [{'id': r[0], 'name': r[1], 'img': r[2]} for r in rows]
    return jsonify(cards)



    query += " ORDER BY c.name"
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    cur.close()@app.route('/api/cards')
def get_cards():
    conn = get_connection()
    cur = conn.cursor()

    rarities = request.args.get('rarities', '').split(',') if request.args.get('rarities') else []
    keywords = request.args.get('keywords', '').split(',') if request.args.get('keywords') else []
    max_energy = request.args.get('max_energy', None, type=int)

    params = []
    # --- INÍCIO DA VERSÃO FINAL E CORRETA DA QUERY ---
    query = """
        SELECT DISTINCT c.id, c.name, c.img
        FROM cards c
        LEFT JOIN card_rarity cr ON c.id = cr.card_id      -- Ligação 1: cards -> card_rarity (usando card_id)
        LEFT JOIN rarity r ON cr.rarity_id = r.id          -- Ligação 2: card_rarity -> rarity (usando rarity_id)
        LEFT JOIN card_keywords ck ON c.id = ck.card_id
        LEFT JOIN keywords k ON ck.keyword_id = k.id
        WHERE 1=1
    """
    # --- FIM DA VERSÃO FINAL ---

    if max_energy is not None:
        query += " AND c.energy <= %s"
        params.append(max_energy)

    # O filtro de raridade está agora reativado com a lógica correta
    if rarities:
        query += " AND r.name = ANY(%s)"
        params.append(rarities)

    if keywords:
        query += """
            AND c.id IN (
                SELECT card_id FROM card_keywords cki
                JOIN keywords ki ON cki.keyword_id = ki.id
                WHERE ki.name = ANY(%s)
                GROUP BY card_id
                HAVING COUNT(DISTINCT ki.name) = %s
            )
        """
        params.append(keywords)
        params.append(len(keywords))

    query += " ORDER BY c.name"
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    cards = [{'id': r[0], 'name': r[1], 'img': r[2]} for r in rows]
    return jsonify(cards)



@app.route('/api/cards/<int:card_id>')
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
            'id': row[0], 'name': row[1], 'subtitle': row[2], 'energy': row[3],
            'might': row[4], 'power': row[5], 'abilities': row[6],
            'flavor': row[7], 'img': row[8],
        }
        return jsonify(card)
    else:
        return jsonify({'error': 'Carta não encontrada'}), 404


# --- Bloco para executar o ficheiro diretamente ---
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)