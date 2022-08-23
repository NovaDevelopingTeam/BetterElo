import sqlite3

def create_db():
    db = sqlite3.connect("betterelo.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS betterelo (telegram_id integer, first_grade_elo INTEGER DEFAULT 300, first_grade_rank STRING, second_grade_elo INTEGER DEFAULT 300, second_grade_rank STRING)")
    cursor.execute("CREATE TABLE IF NOT EXISTS equations (id INTEGER PRIMARY KEY, text STRING, solutions STRING, grade INTEGER, resolves STRING)")
    cursor.execute("CREATE TABLE IF NOT EXISTS langs(telegram_id INTEGER, lang STRING)")
    db.commit()
    db.close()

