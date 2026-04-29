import psycopg


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "snake_final",
    "user": "postgres",
    "password": "260708",
}


def get_connection():
    try:
        return psycopg.connect(**DB_CONFIG)
    except Exception as error:
        print("Database connection error:", error)
        return None


def create_tables():
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()
    return True


def get_or_create_player(username):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO players (username)
        VALUES (%s)
        ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username
        RETURNING id;
        """,
        (username,),
    )
    player_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return player_id


def save_result(username, score, level_reached):
    player_id = get_or_create_player(username)
    if player_id is None:
        return False

    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s);
        """,
        (player_id, int(score), int(level_reached)),
    )
    conn.commit()
    cur.close()
    conn.close()
    return True


def get_personal_best(username):
    conn = get_connection()
    if conn is None:
        return 0

    cur = conn.cursor()
    cur.execute(
        """
        SELECT COALESCE(MAX(game_sessions.score), 0)
        FROM game_sessions
        JOIN players ON players.id = game_sessions.player_id
        WHERE players.username = %s;
        """,
        (username,),
    )
    best = cur.fetchone()[0]
    cur.close()
    conn.close()
    return best


def get_leaderboard():
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            players.username,
            game_sessions.score,
            game_sessions.level_reached,
            TO_CHAR(game_sessions.played_at, 'YYYY-MM-DD HH24:MI')
        FROM game_sessions
        JOIN players ON players.id = game_sessions.player_id
        ORDER BY game_sessions.score DESC, game_sessions.played_at ASC
        LIMIT 10;
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
