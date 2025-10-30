import telebot
import os
import re

TOKEN = "8360820040:AAGSn-lbDRLZeXPaQMg9H-P6DlScg-0a5ZQ"
bot = telebot.TeleBot(TOKEN)

blocked = set()

ATTACK_PATTERNS = [
    "DDoS Port TCP",
    "SQL Injection Attempt",
    "SSH Brute Force",
    "FTP Login Failed",
    "XSS Detected"
]

LOG_PATH = "data/alerts.log"

def count_attacks():
    """
    Menghitung jumlah kemunculan setiap jenis serangan berdasarkan pola yang telah ditentukan
    dalam file log keamanan.

    Fungsi ini membaca file log di lokasi `LOG_PATH`, lalu mencocokkan setiap baris
    dengan pola serangan dalam `ATTACK_PATTERNS`. Setiap baris hanya dihitung untuk
    satu jenis serangan pertama yang cocok.

    Returns:
        dict: Dictionary dengan kunci berupa nama serangan dan nilai berupa jumlah kemunculannya.
              Contoh: {"SQL Injection Attempt": 5, "SSH Brute Force": 2, ...}
    """
    counts = {attack: 0 for attack in ATTACK_PATTERNS}

    if not os.path.exists(LOG_PATH):
        return counts
    
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                for attack in ATTACK_PATTERNS:
                    if attack in line:
                        counts[attack] += 1
                        break
    except Exception:
        pass

    return counts

def risk_level(n):
    """
    Menentukan tingkat risiko berdasarkan jumlah kejadian serangan.

    Skala risiko:
        - <= 10: Low
        - > 10 dan <= 25: Medium
        - > 25: High

    Args:
        n (int): Jumlah kejadian serangan.

    Returns:
        str: Tingkat risiko ("Low", "Medium", atau "High").
    """
    levels = [(10, "Low"), (25, "Medium")]
    for threshold, level in levels:
        if n <= threshold:
            return level
    return "High"

@bot.message_handler(commands=['start'])
def start(m):
    """
    Menangani perintah `/start` dari pengguna Telegram.

    Mengirimkan daftar perintah yang tersedia kepada pengguna dan mencatat aktivitas
    ke konsol untuk tujuan logging.

    Args:
        m (telebot.types.Message): Objek pesan dari Telegram API.
    """
    print(f"Perintah diterima: /start dari user {m.from_user.id}")
    bot.reply_to(m, "Perintah:\n/blockip <IP>\n/changepassword <user> <pass>\n/risikoserangan")

@bot.message_handler(commands=['blockip'])
def block(m):
    """
    Menangani perintah `/blockip` untuk memblokir alamat IP tertentu.

    Memvalidasi format IP (IPv4) dan menambahkannya ke set `blocked` jika valid.
    Memberikan respons sesuai keberhasilan atau kegagalan validasi.

    Args:
        m (telebot.types.Message): Objek pesan dari Telegram API.
    """
    try:
        ip = m.text.split()[1]
        if ip.count('.') == 3 and all(0 <= int(x) <= 255 for x in ip.split('.')):
            blocked.add(ip)
            print(f"IP {ip} diblokir oleh user {m.from_user.id}")
            bot.reply_to(m, f"IP {ip} diblokir.")
        else:
            print(f"Format IP tidak valid dari user {m.from_user.id}: {ip}")
            bot.reply_to(m, "IP tidak valid.")
    except (IndexError, ValueError):
        print(f"Perintah /blockip tidak valid dari user {m.from_user.id}")
        bot.reply_to(m, "Format: /blockip <IP>")

@bot.message_handler(commands=['changepassword'])
def pwd(m):
    """
    Menangani perintah `/changepassword` untuk mengubah kata sandi pengguna.

    Mencatat permintaan perubahan sandi ke konsol (simulasi — tidak benar-benar mengubah sistem).
    Mengharapkan dua argumen: username dan password baru.

    Args:
        m (telebot.types.Message): Objek pesan dari Telegram API.
    """
    try:
        _, u, p = m.text.split(maxsplit=2)
        print(f"Password untuk user '{u}' diubah oleh user {m.from_user.id}")
        bot.reply_to(m, f"Password untuk {u} diubah.")
    except ValueError:
        print(f"Perintah /changepassword tidak valid dari user {m.from_user.id}")
        bot.reply_to(m, "Format: /changepassword <user> <password>")

@bot.message_handler(commands=['risikoserangan'])
def rs(m):
    """
    Menangani perintah `/risikoserangan` untuk menampilkan laporan risiko serangan.

    Menghitung jumlah setiap jenis serangan dari log, menentukan tingkat risiko,
    lalu mengirim ringkasan ke pengguna.

    Args:
        m (telebot.types.Message): Objek pesan dari Telegram API.
    """
    print(f"Laporan risiko serangan diminta oleh user {m.from_user.id}")
    counts = count_attacks()
    msg = "Risiko Serangan:\n"

    for attack in ATTACK_PATTERNS:
        c = counts[attack]
        msg += f"- {attack}: {risk_level(c)} ({c})\n"
    bot.reply_to(m, msg)

bot.polling()