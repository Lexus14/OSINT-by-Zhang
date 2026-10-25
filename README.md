⚡ ZHANG Phone OSINT

ZHANG Phone OSINT adalah toolkit Public OSINT berbasis Python untuk Termux yang membantu melakukan analisis nomor telepon dan pencarian informasi yang tersedia secara publik.

«Version: 6.4
Platform: Termux / Android
Language: Python 3
Author: Muhammad Jeksen»

---

🧬 Features

📱 Phone Analysis

- Phone number normalization
- Country detection
- Prefix detection
- Provider reference
- HLR area reference

🌐 Public Web OSINT

- Google public search
- Exact-match search
- Automatic search URL generation

🔎 Social Public OSINT

- Facebook
- Instagram
- TikTok
- X
- Telegram

🐙 GitHub Public Search

⌕ Google Dork Generator

📊 Reports

- TXT
- JSON
- Timestamp
- Search status

⚡ Fast Scan

- Parallel public endpoint checks
- Lightweight Termux interface

---

🎬 Example

Contoh target:

0812345678910

ZHANG memproses target secara bertahap:

ZHANG › 4

Target number › 0812345678910

⠋ Normalizing phone number...
⠙ Analyzing phone...
⠹ Detecting provider...
⠸ Checking HLR reference...
✓ Analysis complete

[████████████████████] 100%

◈ Phone Analysis

International  │ +62812345678910
Local          │ 0812345678910
Country        │ Indonesia
Prefix         │ 0812
Provider       │ Telkomsel
HLR Reference  │ ...

◎ Public Web OSINT

⠋ Connecting to Google...
⠙ Processing public search...
✓ Google search ready

Status │ OPEN SEARCH

◉ Social Public OSINT

Facebook   ✓
Instagram  ✓
TikTok     ✓
X          ✓
Telegram   ✓

✓ Scan Complete

╔══════════════════════════════════════╗
║          ZHANG SCAN COMPLETE         ║
║       PUBLIC OSINT PROCESSING        ║
╚══════════════════════════════════════╝

«"OPEN SEARCH" hanya menunjukkan bahwa endpoint pencarian dapat diakses.
Itu bukan bukti bahwa nomor ditemukan atau dimiliki oleh seseorang.»

---

🖥️ Menu

[1] Phone Analysis
[2] Public Web OSINT
[3] Social Public OSINT
[4] Search All
[5] Google Dork Generator
[6] GitHub Public Search
[7] About
[0] Exit

---

📦 Installation

Clone repository:

git clone https://github.com/Lexus14/OSINT-by-Zhang.git

Masuk ke folder:

cd OSINT-by-Zhang

Jalankan:

python zhang_phone_osint_v6.4.py

Jika Python belum terpasang:

pkg update
pkg install python

---

🔍 Google Dork Generator

ZHANG dapat membuat query pencarian publik seperti:

"0812345678910"

site:facebook.com "0812345678910"

site:instagram.com "0812345678910"

site:tiktok.com "0812345678910"

site:x.com "0812345678910"

site:t.me "0812345678910"

site:github.com "0812345678910"

---

📊 Reports

ZHANG dapat menghasilkan:

phone_osint_report.txt
phone_osint_report.json

Report berisi:

- Target analysis
- Provider
- HLR reference
- Search URLs
- Search status
- Timestamp
- Disclaimer

---

🛠️ Roadmap

V6.x

- [x] Phone analysis
- [x] Provider reference
- [x] HLR reference
- [x] Google public search
- [x] Social public search
- [x] GitHub public search
- [x] Google dork generator
- [x] TXT report
- [x] JSON report
- [x] Parallel endpoint checks
- [x] Terminal UI

V7 — Intelligence Engine

- [ ] Smart query generation
- [ ] Search result analysis
- [ ] Public evidence extraction
- [ ] Result classification
- [ ] Confidence indicators
- [ ] Improved GitHub intelligence
- [ ] Evidence-based reporting
- [ ] Advanced JSON report

---

⚠️ Disclaimer

ZHANG hanya ditujukan untuk Public OSINT dan informasi yang tersedia secara publik.

Tool ini tidak dirancang untuk:

- mengakses akun pribadi
- mencuri credential
- credential stuffing
- mencari database yang bocor
- mengakses percakapan pribadi
- mengakses WhatsApp pribadi
- stalking
- pelacakan lokasi real-time
- memperoleh data pribadi secara ilegal

HLR hanya merupakan referensi area nomor dan bukan lokasi fisik real-time.

Gunakan ZHANG secara legal, etis, dan bertanggung jawab.

---

👨‍💻 Author

Muhammad Jeksen

ZHANG Phone OSINT V6.4

«Public Intelligence Toolkit for Termux.»

🧰 Prerequisites

Sebelum menjalankan ZHANG, pastikan perangkat memiliki:

- Android dengan Termux
- Python 3.9+
- Git
- Koneksi internet untuk public web search

Recommended Environment

Android
  └── Termux
       ├── Python 3
       └── Git

---

📦 Install Dependencies

Update package repository Termux:

pkg update && pkg upgrade

Install Python dan Git:

pkg install python git

Periksa instalasi:

python --version

git --version

Contoh:

Python 3.x.x
git version 2.x.x

Python Dependencies

ZHANG V6.4 tidak membutuhkan package Python eksternal.

Tool hanya menggunakan Python Standard Library:

re
json
time
urllib
shutil
datetime
concurrent.futures

Jadi tidak perlu menjalankan "pip install".

---

🚀 Installation

Clone repository:

git clone https://github.com/Lexus14/OSINT-by-Zhang.git

Masuk ke directory:

cd OSINT-by-Zhang

Periksa file:

ls

Jalankan ZHANG:

python zhang_phone_osint_v6.4.py

---

🔄 Update

Jika repository sudah pernah di-clone:

cd OSINT-by-Zhang
git pull

Kemudian jalankan kembali:

python zhang_phone_osint_v6.4.py

---

🌐 Internet Requirement

Koneksi internet diperlukan untuk fitur:

- Google Public Search
- Facebook Public Search
- Instagram Public Search
- TikTok Public Search
- X Public Search
- Telegram Public Search
- GitHub Public Search

Phone Analysis dan Google Dork Generator dapat digunakan tanpa melakukan request pencarian web.
