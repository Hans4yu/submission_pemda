
# 📦 ETL Pipeline: Submission Pemda

Proyek ini adalah implementasi ETL (Extract, Transform, Load) pipeline menggunakan Python. Pipeline ini mengambil data, membersihkannya, dan menyimpannya ke beberapa target seperti CSV, PostgreSQL, dan Google Sheets.

---

## 🚀 Fitur

- ✅ Ekstraksi data otomatis (`extract_data`)
- 🔁 Transformasi data ke format final (`transform_data`)
- 💾 Penyimpanan ke:
  - CSV
  - PostgreSQL
  - Google Sheets
- 🧪 Pengujian unit dengan `pytest`
- 📊 Laporan test coverage dengan `pytest-cov`

---

## 🛠️ Instalasi

1. **Clone repo:**
   ```bash
   git clone https://github.com/Hans4yu/submission_pemda.git
   cd submission_pemda
   ```

2. **Buat virtual environment & aktifkan:**
   ```bash
   python -m venv .env
   source .env/bin/activate  # Linux/macOS
   .\.env\Scripts\activate   # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧾 Konfigurasi Database PostgreSQL

### 1. Buat Database dan User (via terminal `psql`):

```sql
-- Masuk sebagai user postgres
psql -U postgres

-- Buat database
CREATE DATABASE etl_db;

-- Buat user khusus ETL
CREATE USER etl_user WITH PASSWORD 'admin';

-- Beri akses penuh ke database
GRANT ALL PRIVILEGES ON DATABASE etl_db TO etl_user;

-- Beri hak CREATE di schema public
\c etl_db
GRANT USAGE, CREATE ON SCHEMA public TO etl_user;

-- (Opsional) Beri hak default untuk SELECT, INSERT, dll
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO etl_user;
```

### 2. Tambahkan URL koneksi di `.env`:

```env
POSTGRES_URL=postgresql://etl_user:admin@localhost:5432/etl_db
```

---

## 🧭 Google Sheets Setup

1. Buat service account dari [Google Cloud Console](https://console.cloud.google.com/)
2. Unduh file credential JSON dan simpan sebagai `google-sheets-api.json`
3. Share spreadsheet ke email service account
4. Tambahkan ke `.env`:

```env
GOOGLE_SHEET_ID=your_spreadsheet_id
GOOGLE_SHEET_JSON_KEY=google-sheets-api.json
```

---

## ▶️ Menjalankan ETL Pipeline

```bash
python main.py
```

---

## 🧪 Menjalankan Test

```bash
pytest -v
```

### Dengan Coverage:
```bash
pytest --cov=utils --cov-report=term-missing tests/
```

### Laporan HTML:
```bash
pytest --cov=utils --cov-report=html
start htmlcov/index.html  # Windows
```

---

## 🧱 Struktur Proyek

```
submission_pemda/
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   ├── test_extract.py
│   ├── test_load.py
│   └── test_transform.py
├── main.py
├── products.csv
├── google-sheets-api.json
├── submission.txt
├── README.md
└── requirements.txt
```

---

## 📄 Lisensi

Proyek ini bebas digunakan untuk edukasi dan pengembangan pribadi. Lisensi dapat ditambahkan sesuai kebutuhan.
