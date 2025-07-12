import os
import asyncio
import httpx
import logging
import nest_asyncio
from dotenv import load_dotenv
from telegram import send_message, send_help_user, send_help_admin, send_document
from db import (
    init_db, add_user, get_user, list_users,
    save_transaction, get_transactions, reset_user_data,
    set_bank_for_user, get_user_bank, user_exists,
    delete_user  # ⬅️ tambahkan ini
)
from excel import export_to_excel
from logger import get_logger

load_dotenv()
nest_asyncio.apply()
logger = get_logger()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
ADMIN_ID = int(os.getenv("ADMIN_ID", "5831560070"))

async def process_update(update):
    try:
        message = update.get("message")
        if not message:
            return

        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        name = message["chat"].get("first_name", "User")

        logger.info(f"📩 Pesan dari {chat_id}: {text}")

        if text.startswith("/start"):
            await send_message(chat_id, f"Halo {name}! 👋\nSelamat datang di *Bot Keuangan*.\nGunakan perintah /newuser untuk mulai.")
            return

        if text.startswith("/help"):
            if chat_id == ADMIN_ID:
                await send_help_admin(chat_id)
            else:
                await send_help_user(chat_id)
            return

        if text.startswith("/newuser"):
            if user_exists(chat_id):
                await send_message(chat_id, "✅ Kamu sudah terdaftar.")
                return
            await send_message(chat_id, "👤 Silakan kirim nama lengkapmu:")
            response = await wait_for_response(chat_id)
            nama = response.get("text", "").strip() or "Tanpa Nama"
            await send_message(chat_id, "🏦 Bank apa yang kamu gunakan? (Contoh: BRI, BNI, BCA)")
            response = await wait_for_response(chat_id)
            bank = response.get("text", "").strip().upper() or "BRI"
            add_user(chat_id, nama, bank)
            await send_message(chat_id, f"✅ Terdaftar sebagai *{nama}* dengan bank *{bank}*", parse_mode="Markdown")
            return

        if text.lower() in ["/bri", "/bni", "/bca"]:
            if not user_exists(chat_id):
                await send_message(chat_id, "🚫 Silakan daftar dulu dengan perintah /newuser")
                return
            bank = text[1:].upper()
            set_bank_for_user(chat_id, bank)
            await send_message(chat_id, f"🏦 Bank aktif diatur ke *{bank}*", parse_mode="Markdown")
            return

        if text == "/listuser" and chat_id == ADMIN_ID:
            users = list_users()
            if not users:
                await send_message(chat_id, "📭 Belum ada pengguna.")
                return
            msg = "📋 *Daftar Pengguna:*\n"
            for uid, nama, bank in users:
                msg += f"🔹 `{uid}` - *{nama}* ({bank})\n"
            await send_message(chat_id, msg, parse_mode="Markdown")
            return
        
        if text.startswith("/hapususer") and chat_id == ADMIN_ID:
            parts = text.split()
            if len(parts) != 2:
                await send_message(chat_id, "❗ Format salah. Gunakan: /hapususer <chat_id>")
                return
            target_id = int(parts[1])
            if not user_exists(target_id):
                await send_message(chat_id, "🚫 Pengguna tidak ditemukan.")
                return
            delete_user(target_id)
            await send_message(chat_id, f"🗑️ Pengguna `{target_id}` berhasil dihapus.", parse_mode="Markdown")
            return

        if text == "/rekap":
            data = get_transactions(chat_id)
            if not data:
                await send_message(chat_id, "📭 Belum ada transaksi.")
                return
            msg = "📊 *Rekap Transaksi:*\n"
            for tanggal, jenis, jumlah, keterangan in data:
                emoji = "➕" if jenis == "masuk" else "➖"
                msg += f"{emoji} Rp{jumlah:,} - {keterangan} ({tanggal})\n"
            await send_message(chat_id, msg, parse_mode="Markdown")
            return

        if text == "/export":
            path = export_to_excel(chat_id)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    await send_document(chat_id, f, "Rekap_Keuangan.xlsx")
                os.remove(path)
            else:
                await send_message(chat_id, "❌ Gagal mengekspor data.")
            return

        if text == "/reset":
            reset_user_data(chat_id)
            await send_message(chat_id, "🗑️ Semua data transaksi berhasil dihapus.")
            return

        # Bukan command, asumsikan transaksi
        if not user_exists(chat_id):
            await send_message(chat_id, "🚫 Silakan daftar dulu dengan /newuser")
            return

        jenis, jumlah, keterangan = classify_transaction(text)
        if jumlah == 0:
            await send_message(chat_id, "⚠️ Format transaksi tidak dikenali. Contoh: `10000 gaji` atau `-5000 makan`", parse_mode="Markdown")
            return

        save_transaction(chat_id, jenis, jumlah, keterangan)
        emoji = "✅" if jenis == "masuk" else "💸"
        await send_message(chat_id, f"{emoji} Tercatat: Rp{jumlah:,} - {keterangan}")

    except Exception as e:
        logger.error(f"❌ Error saat memproses update: {e}")

def classify_transaction(text):
    try:
        parts = text.split()
        jumlah = int(parts[0].replace(".", "").replace(",", ""))
        jenis = "masuk" if jumlah > 0 else "keluar"
        keterangan = " ".join(parts[1:]) if len(parts) > 1 else "Tanpa Keterangan"
        return jenis, abs(jumlah), keterangan
    except:
        return "keluar", 0, "Format tidak dikenal"

async def wait_for_response(chat_id, timeout=60):
    logger.info(f"⏳ Menunggu input dari {chat_id}...")
    for _ in range(timeout * 2):  # timeout dalam detik (interval 0.5s)
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(f"{API_URL}/getUpdates")
                updates = res.json().get("result", [])
                for upd in reversed(updates):
                    msg = upd.get("message", {})
                    if msg.get("chat", {}).get("id") == chat_id:
                        return msg
            except Exception as e:
                logger.warning(f"⚠️ wait_for_response error: {e}")
        await asyncio.sleep(0.5)
    return {"text": ""}

async def polling():
    offset = None
    logger.info("🤖 Bot Keuangan siap digunakan!")
    while True:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{API_URL}/getUpdates", params={"timeout": 10, "offset": offset})
                updates = res.json().get("result", [])
                for upd in updates:
                    offset = upd["update_id"] + 1
                    await process_update(upd)
        except Exception as e:
            err_msg = str(e) if str(e) else repr(e)
            logger.error(f"❌ Gagal polling: {e}")
        await asyncio.sleep(1)

if __name__ == "__main__":
    init_db()
    asyncio.run(polling())
