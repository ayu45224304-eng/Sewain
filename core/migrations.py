def migrate_schema(conn):
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "inventaris" not in tables or "detail_peminjaman" not in tables:
        return

    inventaris_columns = {row[1] for row in conn.execute("PRAGMA table_info(inventaris)")}
    if "harga" not in inventaris_columns:
        conn.execute("ALTER TABLE inventaris ADD COLUMN harga INTEGER NOT NULL DEFAULT 0")

    category_columns = {row[1] for row in conn.execute("PRAGMA table_info(kategori)")}
    initialize_category_codes = "kode" not in category_columns
    if initialize_category_codes:
        conn.execute("ALTER TABLE kategori ADD COLUMN kode TEXT")
    elif conn.execute(
        "SELECT 1 FROM kategori WHERE kode IS NULL OR kode LIKE '__MIGRATE__%' LIMIT 1"
    ).fetchone():
        initialize_category_codes = True
    if initialize_category_codes:
        conn.execute("UPDATE kategori SET kode='__MIGRATE__' || id")
        canonical_categories = (
            "Atribut", "Audio", "Dekorasi", "Fotografi", "Kebersihan",
            "Kelistrikan", "Kesehatan", "Komunikasi", "Konsumsi", "Logistik",
            "Musik", "Pencahayaan", "Perkakas", "Sekretariat", "Visual",
        )
        for number, name in enumerate(canonical_categories, start=1):
            conn.execute(
                "UPDATE kategori SET kode=? WHERE nama=?",
                (f"KAT-{number:03d}", name),
            )
        custom_categories = conn.execute(
            """SELECT id FROM kategori
            WHERE kode LIKE '__MIGRATE__%'
            ORDER BY nama COLLATE NOCASE,id"""
        ).fetchall()
        for number, row in enumerate(custom_categories, start=len(canonical_categories) + 1):
            conn.execute(
                "UPDATE kategori SET kode=? WHERE id=?",
                (f"KAT-{number:03d}", row[0]),
            )
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_kategori_kode ON kategori(kode)")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_inventaris_kode ON inventaris(kode)")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mahasiswa_nim ON mahasiswa(nim)")

    detail_columns = {row[1] for row in conn.execute("PRAGMA table_info(detail_peminjaman)")}
    if "kode_barang" in detail_columns:
        return

    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("ALTER TABLE detail_peminjaman RENAME TO detail_peminjaman_lama")
    conn.execute("""CREATE TABLE detail_peminjaman (
      id INTEGER PRIMARY KEY AUTOINCREMENT, peminjaman_id INTEGER NOT NULL,
      inventaris_id INTEGER, kode_barang TEXT NOT NULL DEFAULT '',
      nama_barang TEXT NOT NULL DEFAULT '', harga_satuan INTEGER NOT NULL DEFAULT 0,
      jumlah INTEGER NOT NULL,
      FOREIGN KEY(peminjaman_id) REFERENCES peminjaman(id) ON DELETE CASCADE,
      FOREIGN KEY(inventaris_id) REFERENCES inventaris(id) ON DELETE SET NULL
    )""")
    conn.execute("""INSERT INTO detail_peminjaman
      (id,peminjaman_id,inventaris_id,kode_barang,nama_barang,harga_satuan,jumlah)
      SELECT d.id,d.peminjaman_id,d.inventaris_id,i.kode,i.nama,i.harga,d.jumlah
      FROM detail_peminjaman_lama d JOIN inventaris i ON i.id=d.inventaris_id""")
    conn.execute("DROP TABLE detail_peminjaman_lama")
    conn.execute("PRAGMA foreign_keys = ON")
