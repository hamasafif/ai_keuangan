import httpx
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def send_message(chat_id, text, parse_mode="Markdown"):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        })

async def send_document(chat_id, file_bytes, filename):
    files = {"document": (filename, file_bytes)}
    data = {"chat_id": chat_id}
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/sendDocument", data=data, files=files)

async def send_help_user(chat_id):
    text = """
📚 *Panduan Pengguna Bot Keuangan* 💸

Berikut ini perintah yang bisa kamu gunakan:

🔹 /newuser → Daftar dan pilih bank
🔹 /bri, /bni, /bca, dll → Ganti bank aktif
🔹 /rekap → Lihat ringkasan transaksi
🔹 /export → Ekspor data ke Excel
🔹 /reset → Hapus semua data
🔹 Ketik nominal + keterangan untuk catat transaksi (contoh: 50000 gaji)

📈 Fitur akan terus bertambah!
"""
    await send_message(chat_id, text)

async def send_help_admin(chat_id):
    text = """
🛠️ *Admin Panel Bot Keuangan* 🧠

Perintah khusus admin:

🧾 /listuser → Lihat semua pengguna
👤 /newuser → Daftarkan pengguna baru
❌ /hapususer → (WIP) Hapus pengguna

Fitur monitoring dan manajemen akan terus dikembangkan! 🚀
"""
    await send_message(chat_id, text)
