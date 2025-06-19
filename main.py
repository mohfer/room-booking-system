import sqlite3

# Inisialisasi Database
def init_db():
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ruangan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL UNIQUE,
            kapasitas INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_peminjam TEXT NOT NULL,
            ruangan_id INTEGER NOT NULL,
            tanggal TEXT NOT NULL,
            jam_mulai TEXT NOT NULL,
            jam_selesai TEXT NOT NULL,
            status TEXT DEFAULT 'aktif',
            FOREIGN KEY (ruangan_id) REFERENCES ruangan (id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS riwayat_peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peminjaman_id INTEGER NOT NULL,
            status TEXT,
            waktu_dibuat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (peminjaman_id) REFERENCES peminjaman (id)
        );
    """)
    cursor.execute("SELECT * FROM admin WHERE username = ?", ('admin',))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        cursor.execute("INSERT INTO ruangan (id, nama, kapasitas) VALUES (?, ?, ?)", ('1', 'Lab Komputer Informatika', '30'))
    conn.commit()
    conn.close()


# Login Admin
def login():
    print("\n=== LOGIN ADMIN TU ===")
    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login berhasil. Selamat datang,", username)
        admin_menu(username)
    else:
        print("Login gagal. Username atau password salah.")


# Menu Admin
def admin_menu(username):
    while True:
        print(f"\n--- MENU ADMIN ({username}) ---")
        print("1. Lihat Daftar Admin")
        print("2. Tambah Admin Baru")
        print("3. Hapus Akun Admin")
        print("4. Kelola Data Ruangan")
        print("5. Kelola Data Peminjaman")
        print("0. Logout")

        choice = input("Pilih menu: ")
        if choice == "1":
            lihat_admin()
        elif choice == "2":
            tambah_admin()
        elif choice == "3":
            hapus_admin(username)
        elif choice == "4":
            menu_ruangan()
        elif choice == "5":
            menu_peminjaman()
        elif choice == "0":
            print("Logout...\n")
            break
        else:
            print("Pilihan tidak valid!")


# CRUD Admin
def lihat_admin():
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM admin")
    for row in cursor.fetchall():
        print(f"- ID: {row[0]}, Username: {row[1]}")
    conn.close()


def tambah_admin():
    print("\n=== Tambah Admin Baru ===")
    user = input("Username baru: ")
    pwd = input("Password: ")
    
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (user, pwd))
        conn.commit()
        print("Admin berhasil ditambahkan!")
    except sqlite3.IntegrityError:
        print("Username sudah digunakan!")
    conn.close()


def hapus_admin(current_user):
    lihat_admin()
    print("\n=== Hapus Akun Admin ===")
    uname = input("Username yang ingin dihapus: ")
    
    if uname == current_user:
        print("Tidak bisa menghapus akun sendiri.")
        return
    
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM admin WHERE username = ?", (uname,))
    
    if cursor.fetchone():
        konfirm = input(f"Yakin hapus '{uname}'? (y/n): ").lower()
        if konfirm == "y":
            cursor.execute("DELETE FROM admin WHERE username = ?", (uname,))
            conn.commit()
            print("Akun dihapus.")
    else:
        print("Username tidak ditemukan.")
    conn.close()


# Menu Ruangan
def menu_ruangan():
    while True:
        print("\n--- MANAJEMEN DATA RUANGAN ---")
        print("1. Lihat Daftar Ruangan")
        print("2. Tambah Ruangan")
        print("3. Ubah Data Ruangan")
        print("4. Hapus Ruangan")
        print("0. Kembali")
        
        choice = input("Pilih menu: ")
        if choice == "1":
            lihat_ruangan()
        elif choice == "2":
            tambah_ruangan()
        elif choice == "3":
            ubah_ruangan()
        elif choice == "4":
            hapus_ruangan()
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid!")


# CRUD Ruangan
def lihat_ruangan():
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ruangan")
    rows = cursor.fetchall()
    
    for r in rows:
        print(f"- ID: {r[0]}, Nama: {r[1]}, Kapasitas: {r[2]}")
    conn.close()


def tambah_ruangan():
    print("\n=== Tambah Ruangan ===")
    nama = input("Nama Ruangan: ")
    kapasitas = input("Kapasitas: ")
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    # Cek nama ruangan
    cursor.execute("SELECT * FROM ruangan WHERE LOWER(TRIM(nama)) = LOWER(TRIM(?))", (nama,))
    checkName = cursor.fetchone()
    
    if checkName:
        print("Nama ruangan sudah ada.")
    else:
        cursor.execute("INSERT INTO ruangan (nama, kapasitas) VALUES (?, ?)", (nama, int(kapasitas)))
        conn.commit()
        conn.close()
        print("Ruangan ditambahkan.")


def ubah_ruangan():
    lihat_ruangan()
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    idr = input("ID Ruangan yang diubah: ")
    cursor.execute("SELECT * FROM ruangan WHERE id = ?", (idr,))
    data = cursor.fetchone()
    
    if data:
        nama = input("Nama baru (biarkan kosong jika tetap): ") or data[1]
        kapasitas_input = input("Kapasitas baru (biarkan kosong jika tetap): ")
        kapasitas = kapasitas_input if kapasitas_input else str(data[2])

        if not kapasitas.isdigit() or int(kapasitas) <= 0:
            print("Kapasitas harus berupa angka positif.")
            conn.close()
            return

        cursor.execute("""
            SELECT * FROM ruangan 
            WHERE LOWER(TRIM(nama)) = LOWER(TRIM(?)) AND id != ?
        """, (nama, idr))
        nama_sudah_ada = cursor.fetchone()

        if nama_sudah_ada:
            print("Nama ruangan sudah digunakan oleh ruangan lain.")
        else:
            cursor.execute("UPDATE ruangan SET nama = ?, kapasitas = ? WHERE id = ?", (nama, int(kapasitas), idr))
            conn.commit()
            print("Ruangan berhasil diubah.")
    else:
        print("ID tidak ditemukan.")
    
    conn.close()


def hapus_ruangan():
    idr = input("ID Ruangan yang dihapus: ")
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ruangan WHERE id = ?", (idr,))
    data = cursor.fetchone()
    
    if data:
        konfirm = input(f"Yakin hapus '{data[1]}'? (y/n): ").lower()
        if konfirm == "y":
            cursor.execute("DELETE FROM ruangan WHERE id = ?", (idr,))
            conn.commit()
            print("Ruangan dihapus.")
    else:
        print("ID tidak ditemukan.")
    conn.close()


# Menu Peminjaman
def menu_peminjaman():
    while True:
        print("\n--- MANAJEMEN PEMINJAMAN ---")
        print("1. Lihat Semua Peminjaman")
        print("2. Tambah Peminjaman")
        print("3. Edit Peminjaman")
        print("4. Selesaikan Peminjaman")
        print("5. Riwayat Peminjaman")
        print("0. Kembali")

        choice = input("Pilih menu: ")
        if choice == "1":
            lihat_peminjaman()
        elif choice == "2":
            tambah_peminjaman()
        elif choice == "3":
            ubah_peminjaman()
        elif choice == "4":
            selesaikan_peminjaman()
        elif choice == "5":
            riwayat_peminjaman()
        elif choice == "0":
            break


# CRUD Peminjaman
def lihat_peminjaman():
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.nama_peminjam, r.nama, p.tanggal, p.jam_mulai, p.jam_selesai, p.status
        FROM peminjaman p JOIN ruangan r ON p.ruangan_id = r.id
        WHERE p.status = 'aktif'
        ORDER BY p.tanggal, p.jam_mulai
    """)
    
    for d in cursor.fetchall():
        print(f"- ID: {d[0]}, {d[1]} pinjam {d[2]}, {d[3]} pukul {d[4]} - {d[5]}")
    conn.close()


def tambah_peminjaman():
    print("\n=== Tambah Peminjaman ===")
    nama = input("Nama Peminjam: ")
    lihat_ruangan()
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    
    rid = input("ID Ruangan: ")
    
    cursor.execute("SELECT * FROM ruangan WHERE id = ?", (rid,))
    ruangan = cursor.fetchone()
    if not ruangan:
        print("ID ruangan tidak ditemukan.")
        conn.close()
        return
    
    tanggal = input("Tanggal (DD-MM-YYYY): ")
    jm = input("Jam Mulai (HH:MM): ")
    js = input("Jam Selesai (HH:MM): ")

    if bentrok_jadwal(rid, tanggal, jm, js):
        print("Jadwal bentrok. Pilih waktu lain.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO peminjaman (nama_peminjam, ruangan_id, tanggal, jam_mulai, jam_selesai)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, rid, tanggal, jm, js))
    idp = cursor.lastrowid

    cursor.execute("""
        INSERT INTO riwayat_peminjaman (peminjaman_id, status)
        VALUES (?, ?)
    """, (idp, 'pinjam'))

    conn.commit()
    conn.close()
    print("Peminjaman ditambahkan.")
    

def ubah_peminjaman():
    lihat_peminjaman()
    idp = input("ID yang diubah: ")
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM peminjaman WHERE id = ? AND status = ?", (idp, 'aktif'))
    data = cursor.fetchone()
    if not data:
        print("ID peminjaman tidak ditemukan.")
        conn.close()
        return

    nama = input("Nama (kosongkan jika tetap): ") or data[1]
    lihat_ruangan()
    rid = input("ID Ruangan: ") or str(data[2])

    cursor.execute("SELECT * FROM ruangan WHERE id = ?", (rid,))
    ruangan = cursor.fetchone()
    if not ruangan:
        print(f"ID Ruangan '{rid}' tidak ditemukan. Silakan masukkan ID yang valid.")
        conn.close()
        return

    tanggal = input("Tanggal (DD-MM-YYYY): ") or data[3]
    jm = input("Jam Mulai (HH:MM): ") or data[4]
    js = input("Jam Selesai (HH:MM): ") or data[5]

    if bentrok_jadwal(rid, tanggal, jm, js, id_ignore=idp):
        print("Jadwal bentrok dengan peminjaman lain.")
        conn.close()
        return

    cursor.execute("""
        UPDATE peminjaman
        SET nama_peminjam = ?, ruangan_id = ?, tanggal = ?, jam_mulai = ?, jam_selesai = ?
        WHERE id = ?
    """, (nama, rid, tanggal, jm, js, idp))

    conn.commit()
    conn.close()
    print("Peminjaman berhasil diubah.")


def selesaikan_peminjaman():
    lihat_peminjaman()
    idp = input("ID yang sudah selesai: ")
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM peminjaman WHERE id = ? AND status = ?", (idp, 'aktif'))
    data = cursor.fetchone()

    if data:
        cursor.execute("UPDATE peminjaman SET status = 'selesai' WHERE id = ?", (idp,))
        cursor.execute("INSERT INTO riwayat_peminjaman (peminjaman_id, status) VALUES (?, ?)", (idp, 'selesai pinjam'))
        conn.commit()
        print("Peminjaman diselesaikan.")
    else:
        print("ID tidak ditemukan.")
    conn.close()
    
    
def riwayat_peminjaman():
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            h.id,
            p.nama_peminjam,
            h.status,
            r.nama AS nama_ruangan,
            p.tanggal,
            p.jam_mulai,
            p.jam_selesai,
            h.waktu_dibuat
        FROM
            riwayat_peminjaman h
        JOIN peminjaman p ON h.peminjaman_id = p.id
        JOIN ruangan r ON p.ruangan_id = r.id
        ORDER BY h.waktu_dibuat DESC;
    """)
    
    for d in cursor.fetchall():
        print(f"- ID: {d[0]}, {d[1]} {d[2]} {d[3]}, Tanggal {d[4]}, Jam {d[5]} - {d[6]}, dicatat: {d[7]}")
    
    conn.close()


# Cek bentrok jadwal otomatis
def bentrok_jadwal(rid, tanggal, mulai, selesai, id_ignore=None):
    conn = sqlite3.connect("kampus.db")
    cursor = conn.cursor()
    query = """
        SELECT * FROM peminjaman
        WHERE ruangan_id = ? AND tanggal = ? AND (jam_mulai < ? AND jam_selesai > ?)
    """
    params = (rid, tanggal, selesai, mulai)
    if id_ignore:
        query += " AND id != ?"
        params += (id_ignore,)
    cursor.execute(query, params)
    return cursor.fetchone() is not None


# Main Menu
if __name__ == "__main__":
    init_db()
    while True:
        print("\n=== APLIKASI PEMINJAMAN RUANGAN ===")
        print("1. Login Admin")
        print("2. Keluar")
        pilih = input("Pilih: ")
        if pilih == "1":
            login()
        elif pilih == "2":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")