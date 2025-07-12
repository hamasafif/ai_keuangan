# 💰 AI Keuangan Telegram Bot 🤖📊

Bot Telegram cerdas untuk **mencatat, menganalisis, dan mengelola keuangan pribadi** secara otomatis menggunakan bantuan AI! 🧠⚡

---

## 🚀 Fitur Utama

✨ Bot ini memiliki banyak fitur berguna yang bisa kamu akses langsung dari Telegram:

| Perintah | Fungsi |
|---------|--------|
| `/newuser` 👤 | Daftarkan diri sebagai pengguna baru |
| `/catat` 📝 | Catat transaksi harianmu |
| `/rekap` 📄 | Tampilkan rekap semua transaksi |
| `/saldo` 💰 | Lihat saldo terakhir (masuk - keluar) |
| `/limit` 🚦 | Tetapkan batas pengeluaran |
| `/analisa` 📊 | Gunakan AI untuk menganalisis kebiasaan finansialmu |
| `/grafik` 📈 | Lihat grafik keuanganmu |
| `/export` 📁 | Ekspor semua transaksi ke file Excel |
| `/reset` 🧹 | Hapus seluruh data transaksi |
| `Admin Only 👑` | CRUD user dan manajemen kontrol bot |

---

## 🧠 Kecerdasan Buatan

Bot ini menggunakan **AI** (OpenRouter API) untuk:
- Mengelompokkan transaksi otomatis (pemasukan/pengeluaran)
- Menganalisis kebiasaan keuangan
- Memberi rekomendasi pengelolaan uang

---

## 🛠️ Teknologi yang Digunakan

- 🐍 Python 3
- 🤖 [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- 🧠 OpenRouter API (untuk AI)
- 🗃️ MySQL (untuk penyimpanan data)
- 📦 Docker (siap deploy)
- 📈 Matplotlib (untuk grafik)
- 📊 pandas + openpyxl (untuk export Excel)
- 🧪 nest_asyncio (untuk manajemen event loop Telegram)

---

## ⚙️ Cara Menjalankan

### 1. Clone Repo

```bash
git clone https://github.com/hamasafif/ai_keuangan.git
cd ai_keuangan
```

Buat file .env di root project:
```bash
BOT_TOKEN=isi_token_bot_telegrammu
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=passwordmu
DB_NAME=ai_keuangan
AI_API_KEY=isi_apimu
AI_MODEL=gpt-3.5-turbo
```

🙋 Kontribusi
Pull request terbuka! 💡
Ingin menambahkan fitur baru, memperbaiki bug, atau membuat UI Web? Silakan kontribusi! 🎉

👨‍💻 Dibuat oleh
WR Junior
Made with ❤️ + ☕ + 🧠

📄 Lisensi
MIT License © 2025
