import sqlite3

DATABASE_NAME = "services_bot.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)

  def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            name TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT UNIQUE NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_number TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            details TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (service_id) REFERENCES services(service_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_status_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            old_status TEXT,
            new_status TEXT NOT NULL,
            changed_by INTEGER,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES requests(request_id)
        )
    """)

    connection.commit()
    
    connection.close()
    
def seed_services():
    connection = get_connection()
    cursor = connection.cursor()

    services = [
        "🛠 الصيانة",
        "🛒 الشراء",
        "💰 البيع",
        "⚙️ قطع الغيار",
        "🔧 التركيب",
        "💬 الاستشارات"
    ]

    for service in services:
        cursor.execute(
            "INSERT OR IGNORE INTO services (service_name) VALUES (?)",
            (service,)
        )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_database()
    seed_services()
    print("Database initialized successfully.")
