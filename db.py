import os
import mysql.connector
from dotenv import load_dotenv
import sqlite3

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Tabel pengguna
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            nama TEXT,
            bank TEXT
        )
    ''')

    # Tabel transaksi
    c.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            tanggal TEXT,
            jenis TEXT,
            jumlah INTEGER,
            keterangan TEXT
        )
    ''')

    conn.commit()
    conn.close()

def user_exists(chat_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE chat_id = %s", (chat_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return bool(result)

def add_user(chat_id, nama, bank):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (chat_id, nama, bank) VALUES (%s, %s, %s)", (chat_id, nama, bank))
    conn.commit()
    cur.close()
    conn.close()

def get_user(chat_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def list_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT chat_id, nama, bank FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def set_bank_for_user(chat_id, bank):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET bank = %s WHERE chat_id = %s", (bank, chat_id))
    conn.commit()
    cur.close()
    conn.close()

def get_user_bank(chat_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT bank FROM users WHERE chat_id = %s", (chat_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def save_transaction(chat_id, jenis, jumlah, keterangan):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transaksi (chat_id, jenis, jumlah, keterangan)
        VALUES (%s, %s, %s, %s)
    """, (chat_id, jenis, jumlah, keterangan))
    conn.commit()
    cur.close()
    conn.close()

def get_transactions(chat_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT tanggal, jenis, jumlah, keterangan
        FROM transaksi
        WHERE chat_id = %s
        ORDER BY tanggal DESC
    """, (chat_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_transactions_by_user(chat_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT tanggal, jenis, jumlah, keterangan
        FROM transaksi
        WHERE chat_id = %s
        ORDER BY tanggal ASC
    """, (chat_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def reset_user_data(chat_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM transaksi WHERE chat_id = %s", (chat_id,))
    conn.commit()
    cur.close()
    conn.close()

def delete_user(chat_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))
    c.execute("DELETE FROM transaksi WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

