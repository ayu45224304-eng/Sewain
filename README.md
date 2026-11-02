# Sewain — Sistem Peminjaman Inventaris UKM

Aplikasi admin berbasis Streamlit untuk mencatat inventaris, kategori, mahasiswa/peminjam, peminjaman, pengembalian, dan laporan.

## Menjalankan di VS Code

1. Ekstrak ZIP ini.
2. Buka folder `InvenUKM` di VS Code.
3. Pastikan Python 3.10+ terpasang.
4. Buka Terminal di VS Code, lalu jalankan:

   ```bash
   python -m venv .venv
   ```

   Aktifkan environment:
   - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
   - Windows CMD: `.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`

5. Instal dependensi:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Jalankan aplikasi:

   ```bash
   streamlit run app.py
   ```

Di VS Code, buka terminal baru setelah folder proyek dibuka. Workspace akan memilih `.venv` dan mengaktifkannya otomatis, sehingga perintah `streamlit` tersedia. Jika terminal yang sedang terbuka belum mengaktifkan environment, jalankan aktivasi secara manual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Aplikasi akan terbuka di browser. Pengaturan otomatis ini berlaku untuk terminal terintegrasi VS Code; di terminal lain, aktifkan `.venv` terlebih dahulu.

Aplikasi terbuka langsung tanpa halaman login. Database SQLite akan dibuat otomatis pada `data/invenukm.db`.

## Deploy ke Streamlit Community Cloud

1. Buat repositori GitHub baru, lalu unggah folder proyek ini. Jangan unggah
   `.venv`; folder tersebut sudah dicantumkan di `.gitignore`.
2. Buka <https://share.streamlit.io>, masuk dengan GitHub, lalu pilih
   **Create app**.
3. Pilih repositori dan cabang GitHub proyek, isi:
   - **Main file path:** `app.py`
   - **App URL:** pilih nama aplikasi yang tersedia
4. Pilih **Deploy**. Streamlit akan memasang dependency dari `requirements.txt`.

Database SQLite tidak dipakai sebagai penyimpanan produksi permanen pada
Streamlit Community Cloud. Perubahan data dapat hilang ketika aplikasi direstart
atau container dibuat ulang. Untuk demo, aplikasi membuat database baru secara
otomatis dari data contoh. Untuk penggunaan produksi, gunakan hosting dengan
volume disk persisten atau pindahkan penyimpanan ke database eksternal seperti
PostgreSQL.
