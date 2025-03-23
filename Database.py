import sqlite3

class Database:
    def __init__(self, db_name="blockchain.db"):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        """Membuat database dan tabel jika belum ada"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS blocks (
                            block_index INTEGER PRIMARY KEY,
                            previous_hash TEXT,
                            merkle_root TEXT,
                            owner TEXT,
                            timestamp REAL,
                            nonce INTEGER,
                            hash TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT,
                            content TEXT,
                            hash TEXT)''')
        conn.commit()
        conn.close()

    def save_block(self, block):
        """Menyimpan blok ke database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO blocks (block_index, previous_hash, merkle_root, owner, timestamp, nonce, hash)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (block.block_index, block.previous_hash, block.merkle_root, block.owner, block.timestamp, block.nonce, block.hash))
        conn.commit()
        conn.close()

    def load_blocks(self):
        """Mengambil semua blok dari database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT block_index, previous_hash, merkle_root, owner, timestamp, nonce, hash FROM blocks ORDER BY block_index')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_document(self, filename, content, doc_hash):
        """Menyimpan dokumen ke database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO documents (filename, content, hash) VALUES (?, ?, ?)''',
                       (filename, content, doc_hash))
        conn.commit()
        conn.close()

    def get_document_hash(self, filename):
        """Mengambil hash dari dokumen berdasarkan nama file"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT hash FROM documents WHERE filename = ?', (filename,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None


