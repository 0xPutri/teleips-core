# TeleIPS Core

Proyek ini merupakan **implementasi simulasi** dari penelitian berjudul: **"Network Attack Detection Using Intrusion Detection System Utilizing Snort Based on Telegram"** oleh Juan Adi Dharma & Rino (2023), *Bit-Tech, Vol. 6, No. 2*.

Karena keterbatasan lingkungan (tidak menggunakan Linux, Snort, atau iptables secara langsung), sistem ini **mensimulasikan logika inti** dari penelitian tersebut menggunakan Python murni, dengan fokus pada tiga fitur utama:

1. **Deteksi serangan** (simulasi log berbasis waktu)  
2. **Respons melalui Telegram**:  
   - Blokir IP (`/blockip <IP>`)  
   - Ganti password (`/changepassword <user> <pass>`)  
3. **Klasifikasi risiko serangan** ke dalam tiga kategori:  
   - **Low**: 1–10 kali terdeteksi  
   - **Medium**: 11–20 kali  
   - **High**: >20 kali 

> ⚠️ **Catatan**: Ini adalah **simulasi fungsional**, bukan sistem produksi. Tidak ada integrasi dengan Snort, iptables, atau bash shell asli. Tujuannya adalah memahami arsitektur dan mekanisme respons berbasis Telegram sebagaimana diusulkan dalam jurnal.

## Contoh Output Nyata

### Perintah `/risikoserangan`

```
Risiko Serangan:
- DDoS Port TCP: Medium (11)
- SQL Injection Attempt: Low (9)
- SSH Brute Force: Low (8)
- FTP Login Failed: Low (10)
- XSS Detected: Low (6)
```

### Perintah `/blockip 192.168.1.100`

```
IP 192.168.1.121 diblokir.
```

### Perintah `/changepassword admin secure123`

```
Password untuk admin diubah.
```

## Cara Menjalankan

1. Ganti `BOT_TOKEN` di `src/bot.py` dengan token dari [@BotFather](https://t.me/BotFather)
2. Jalankan dua terminal terpisah:
   
   ```bash
   python src/simulator.py    # menghasilkan log serangan
   python src/bot.py          # menjalankan bot Telegram
   ```
3. Gunakan perintah di Telegram untuk menguji fitur.

## Referensi

Dharma, J. A., & Rino. (2023). Network Attack Detection Using Intrusion Detection System Utilizing Snort Based on Telegram. *Bit-Tech*, 6(2), 120–130.  
Tersedia di: [https://jurnal.kdi.or.id/index.php/bt/article/view/943](https://jurnal.kdi.or.id/index.php/bt/article/view/943)