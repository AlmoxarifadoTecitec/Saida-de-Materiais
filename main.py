import os
import sys
import sqlite3
from datetime import datetime
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Database path
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'empresa.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_retiradas_table():
    """Create retiradas table if it doesn't exist"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS retiradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            observacao TEXT,
            data_retirada DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pendente',
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id),
            FOREIGN KEY (material_id) REFERENCES materiais (id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the retiradas table
init_retiradas_table()

@app.route('/api/funcionarios', methods=['GET'])
def get_funcionarios():
    search = request.args.get('q', '')
    conn = get_db_connection()
    if search:
        funcionarios = conn.execute(
            'SELECT * FROM funcionarios WHERE nome LIKE ? OR apelido LIKE ? ORDER BY nome',
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        funcionarios = conn.execute('SELECT * FROM funcionarios ORDER BY nome').fetchall()
    conn.close()
    return jsonify([dict(row) for row in funcionarios])

@app.route('/api/materiais', methods=['GET'])
def get_materiais():
    search = request.args.get('q', '')
    conn = get_db_connection()
    if search:
        materiais = conn.execute(
            'SELECT * FROM materiais WHERE item LIKE ? OR codigo LIKE ? ORDER BY item LIMIT 50',
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        materiais = conn.execute('SELECT * FROM materiais ORDER BY item LIMIT 50').fetchall()
    conn.close()
    return jsonify([dict(row) for row in materiais])

@app.route('/api/retiradas', methods=['POST'])
def criar_retirada():
    data = request.json
    conn = get_db_connection()
    
    try:
        conn.execute('''
            INSERT INTO retiradas (funcionario_id, material_id, quantidade, observacao)
            VALUES (?, ?, ?, ?)
        ''', (data['funcionario_id'], data['material_id'], data['quantidade'], data.get('observacao', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Retirada registrada com sucesso!'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/retiradas', methods=['GET'])
def get_retiradas():
    status = request.args.get('status', 'all')
    conn = get_db_connection()
    
    if status == 'pendente':
        query = '''
            SELECT r.*, f.nome as funcionario_nome, f.apelido as funcionario_apelido,
                   m.codigo as material_codigo, m.item as material_item
            FROM retiradas r
            JOIN funcionarios f ON r.funcionario_id = f.id
            JOIN materiais m ON r.material_id = m.id
            WHERE r.status = 'pendente'
            ORDER BY r.data_retirada DESC
        '''
    else:
        query = '''
            SELECT r.*, f.nome as funcionario_nome, f.apelido as funcionario_apelido,
                   m.codigo as material_codigo, m.item as material_item
            FROM retiradas r
            JOIN funcionarios f ON r.funcionario_id = f.id
            JOIN materiais m ON r.material_id = m.id
            ORDER BY r.data_retirada DESC
        '''
    
    retiradas = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in retiradas])

@app.route('/api/retiradas/<int:retirada_id>/concluir', methods=['PUT'])
def concluir_retirada(retirada_id):
    conn = get_db_connection()
    conn.execute('UPDATE retiradas SET status = "concluida" WHERE id = ?', (retirada_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Retirada marcada como concluída!'})

@app.route('/api/retiradas/<int:retirada_id>', methods=['DELETE'])
def apagar_retirada(retirada_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM retiradas WHERE id = ?', (retirada_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Retirada apagada com sucesso!'})

@app.route('/api/retiradas/apagar-todas-pendencias', methods=['DELETE'])
def apagar_todas_pendencias():
    conn = get_db_connection()
    conn.execute('DELETE FROM retiradas WHERE status = "pendente"')
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Todas as pendências foram apagadas com sucesso!'})

@app.route('/api/retiradas/limpar-historico', methods=['DELETE'])
def limpar_historico():
    conn = get_db_connection()
    conn.execute('DELETE FROM retiradas WHERE status = "concluida"')
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Histórico limpo com sucesso!'})

@app.route('/api/pendencias/count', methods=['GET'])
def count_pendencias():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM retiradas WHERE status = "pendente"').fetchone()[0]
    conn.close()
    return jsonify({'count': count})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

