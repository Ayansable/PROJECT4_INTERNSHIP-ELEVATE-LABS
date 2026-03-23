import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# malicious IP table
cursor.execute("""
CREATE TABLE IF NOT EXISTS malicious_ips (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ip TEXT
)
""")

# scan logs
cursor.execute("""
CREATE TABLE IF NOT EXISTS scan_logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ip TEXT,
country TEXT,
isp TEXT,
result TEXT
)
""")

# admin table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

# default admin
cursor.execute("""
INSERT INTO admin (username,password)
SELECT 'admin','admin123'
WHERE NOT EXISTS (
SELECT 1 FROM admin WHERE username='admin'
)
""")

conn.commit()
conn.close()

print("Database Ready")