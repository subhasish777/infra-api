from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS servers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    ip VARCHAR(255) NOT NULL UNIQUE,
    os VARCHAR(255) NOT NULL
)
""")

connection.commit()
connection.close()

print("Database schema created successfully")