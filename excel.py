import os
import tempfile
from openpyxl import Workbook
from db import get_transactions_by_user

def export_to_excel(chat_id):
    data = get_transactions_by_user(chat_id)
    if not data:
        return None

    wb = Workbook()
    ws = wb.active
    ws.title = "Transaksi"

    # Header
    ws.append(["Tanggal", "Jenis", "Jumlah", "Keterangan"])

    for row in data:
        ws.append(row)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    wb.save(temp_file.name)
    return temp_file.name
