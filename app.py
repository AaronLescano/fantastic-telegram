from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Amoramoramor123@'
app.config['MYSQL_DB'] = 'football_stats'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicializar MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

# Ruta para obtener todos los jugadores
@app.route('/players', methods=['GET'])
def get_players():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM players")
    players = cur.fetchall()
    return {'players': players}

@app.route('/players', methods=['POST'])
def add_players():
    players = request.json
    cur = mysql.connection.cursor()

    for player in players:
        cur.execute("""
            INSERT INTO players (name, team, position, games_played, goals, assists, yellow_cards, red_cards)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            player['name'], player['team'], player['position'],
            player['games_played'], player['goals'], player['assists'],
            player['yellow_cards'], player['red_cards']
        ))

    mysql.connection.commit()
    return jsonify({'message': 'Players added successfully!'})

# Ruta para obtener un jugador específico basado en su ID
@app.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM players WHERE id = %s", (id,))
    player = cur.fetchone()
    if player:
        return jsonify({'player': player})
    else:
        return jsonify({'message': 'Player not found'}), 404

# Ruta para actualizar los detalles de un jugador existente
@app.route('/players/<int:id>', methods=['PUT'])
def update_player(id):
    cur = mysql.connection.cursor()
    player_details = request.json
    cur.execute("""
        UPDATE players
        SET name = %s, team = %s, position = %s, games_played = %s, goals = %s, assists = %s, yellow_cards = %s, red_cards = %s
        WHERE id = %s
    """, (
        player_details['name'], player_details['team'], player_details['position'],
        player_details['games_played'], player_details['goals'], player_details['assists'],
        player_details['yellow_cards'], player_details['red_cards'], id
    ))
    mysql.connection.commit()
    return jsonify({'message': 'Player updated successfully!'})

# Ruta para eliminar un jugador de la base de datos
@app.route('/players/<int:id>', methods=['DELETE'])
def delete_player(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM players WHERE id = %s", (id,))
    mysql.connection.commit()
    return jsonify({'message': 'Player deleted successfully!'})

# Ruta para calcular el Promedio de Goles por Partido
@app.route('/average_goals_per_game/<int:id>', methods=['GET'])
def average_goals_per_game(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, goals, games_played FROM players WHERE id = %s AND games_played > 0", (id,))
    player = cur.fetchone()
    if player:
        avg_goals_per_game = player['goals'] / player['games_played']
        interpretation = f"{player['name']} tiene un promedio de {avg_goals_per_game:.2f} goles por partido. Esto significa que, en promedio, {player['name']} marca casi {avg_goals_per_game:.2f} gol(es) por cada partido jugado."
        return jsonify({'average_goals_per_game': avg_goals_per_game, 'interpretation': interpretation})
    else:
        return jsonify({'message': 'Player not found or no games played'})


# Ruta para calcular el Promedio de Asistencias por Partido
@app.route('/average_assists_per_game/<int:id>', methods=['GET'])
def average_assists_per_game(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, assists, games_played FROM players WHERE id = %s AND games_played > 0", (id,))
    player = cur.fetchone()
    if player:
        avg_assists_per_game = player['assists'] / player['games_played']
        interpretation = f"{player['name']} tiene un promedio de {avg_assists_per_game:.2f} asistencias por partido. Esto significa que, en promedio, {player['name']} realiza casi {avg_assists_per_game:.2f} asistencia(s) por cada partido jugado."
        return jsonify({'average_assists_per_game': avg_assists_per_game, 'interpretation': interpretation})
    else:
        return jsonify({'message': 'Player not found or no games played'})


# Ruta para calcular el Porcentaje de Goles del Equipo
@app.route('/goal_percentage/<int:id>', methods=['GET'])
def goal_percentage(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, goals, team FROM players WHERE id = %s", (id,))
    player = cur.fetchone()
    if player:
        cur.execute("SELECT SUM(goals) AS total_goals FROM players WHERE team = %s", (player['team'],))
        team_goals = cur.fetchone()
        if team_goals['total_goals'] > 0:
            goal_percentage = (player['goals'] / team_goals['total_goals']) * 100
            interpretation = f"{player['name']} ha contribuido con el {goal_percentage:.2f}% de los goles totales de su equipo, {player['team']}."
            return jsonify({'goal_percentage': goal_percentage, 'interpretation': interpretation})
        else:
            return jsonify({'message': 'No goals scored by the team'})
    else:
        return jsonify({'message': 'Player not found'})


# Ruta para calcular el Ratio de Tarjetas (amarillas + rojas) por Partido
@app.route('/card_ratio/<int:id>', methods=['GET'])
def card_ratio(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, yellow_cards, red_cards, games_played FROM players WHERE id = %s AND games_played > 0", (id,))
    player = cur.fetchone()
    if player:
        card_ratio_per_game = (player['yellow_cards'] + player['red_cards']) / player['games_played']
        interpretation = f"{player['name']} tiene un promedio de {card_ratio_per_game:.2f} tarjetas por partido. Esto significa que, en promedio, {player['name']} recibe {card_ratio_per_game:.2f} tarjeta(s) por cada partido jugado."
        return jsonify({'card_ratio_per_game': card_ratio_per_game, 'interpretation': interpretation})
    else:
        return jsonify({'message': 'Player not found or no games played'})
if __name__ == '__main__':
    app.run(debug=True)
