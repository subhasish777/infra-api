from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS servers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    ip TEXT NOT NULL UNIQUE,
    os TEXT NOT NULL
)
""")

# Optional sample data
cursor.execute("""
INSERT OR IGNORE INTO servers (name, ip, os)
VALUES ('web-server', '192.168.1.10', 'Ubuntu')
""")

cursor.execute("""
INSERT OR IGNORE INTO servers (name, ip, os)
VALUES ('db-server', '192.168.1.20', 'Rocky Linux')
""")

connection.commit()
connection.close()

print("Database initialized successfully")