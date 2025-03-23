import hashlib
import json
import time
from database import Database  # Pastikan ini ada

class Block:
    def __init__(self, block_index, previous_hash, merkle_root, owner, timestamp=None, nonce=0):
        self.block_index = block_index
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.owner = owner
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "block_index": self.block_index,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "owner": self.owner,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block Mined: {self.hash}")

class Blockchain:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.db = Database()  # Gunakan handler database
        self.chain = self.load_blocks()  # Gantilah load_blocks_from_db()
        if not self.chain:
            genesis_block = self.create_genesis_block()
            self.chain = [genesis_block]
            self.db.save_block(genesis_block)  # Simpan genesis block ke database

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Merkle Root", "System", time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data_list, owner):
        merkle_root = merkle_tree([generate_document_hash(data) for data_list in data_list])
        new_block = Block(len(self.chain), self.get_latest_block().hash, merkle_root, owner)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.db.save_block(new_block)  # Simpan blok ke database

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def load_blocks(self):  # FIXED: Tidak ada lagi load_blocks_from_db()
        rows = self.db.load_blocks()
        return [Block(*row) for row in rows] if rows else []

# Fungsi untuk menghasilkan hash dari dokumen
def generate_document_hash(document_content):
    return hashlib.sha256(document_content.encode()).hexdigest()

# Fungsi untuk membuat Merkle Tree
def merkle_tree(data_list):
    if len(data_list) == 1:
        return data_list[0]

    new_level = []
    for i in range(0, len(data_list), 2):
        if i + 1 < len(data_list):
            new_level.append(generate_document_hash(data_list[i] + data_list[i + 1]))
        else:
            new_level.append(generate_document_hash(data_list[i] + data_list[i]))  # Jika ganjil, gandakan terakhir

    return merkle_tree(new_level)

# Example Usage
blockchain = Blockchain()

# Menambahkan dokumen ke database
doc1_hash = blockchain.db.add_document("kontrak_a.txt", "Isi dokumen Kontrak A", generate_document_hash("Isi dokumen Kontrak A"))
doc2_hash = blockchain.db.add_document("kontrak_b.txt", "Isi dokumen Kontrak B", generate_document_hash("Isi dokumen Kontrak B"))

# Mengambil hash dari dokumen dan menambahkannya ke blockchain
blockchain.add_block(["Isi dokumen Kontrak A", "Isi dokumen Kontrak B"], "Alice")

# Cek apakah blockchain valid
print("Blockchain valid?", blockchain.is_chain_valid())
