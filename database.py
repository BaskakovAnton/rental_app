import sqlite3

DATABASE_NAME = 'rental.db'

def create_connection():
    """Создает подключение к базе данных."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    return conn

def create_tables(conn):
    """Создает таблицы для хранения информации."""
    try:
        cursor = conn.cursor()

        # Таблица для велосипедов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bikes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bike_name TEXT NOT NULL,
                bike_type TEXT,  -- Например, горный, городской, детский
                bike_size TEXT,  -- Размер рамы
                rental_price REAL NOT NULL,
                availability INTEGER DEFAULT 1 -- 1 = доступен, 0 = в аренде
            )
        """)

        # Таблица для клиентов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone_number TEXT,
                email TEXT
            )
        """)

        # Таблица для аренд
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bike_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                rental_date TEXT NOT NULL,
                return_date TEXT,
                rental_fee REAL NOT NULL,
                status TEXT DEFAULT 'Активно',  -- Активно, Завершено
                FOREIGN KEY (bike_id) REFERENCES bikes(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")

# Функции для работы с таблицей bikes
def insert_bike(conn, bike):
    sql = """
        INSERT INTO bikes(bike_name, bike_type, bike_size, rental_price, availability)
        VALUES(?,?,?,?,?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, bike)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при вставке велосипеда: {e}")
        return None

def select_all_bikes(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bikes")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Ошибка при выборке велосипедов: {e}")
        return []

def update_bike(conn, bike_id, bike):
    sql = """
        UPDATE bikes
        SET bike_name = ?,
            bike_type = ?,
            bike_size = ?,
            rental_price = ?,
            availability = ?
        WHERE id = ?
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (*bike, bike_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении велосипеда: {e}")

def delete_bike(conn, bike_id):
    sql = "DELETE FROM bikes WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (bike_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при удалении велосипеда: {e}")

# Функции для работы с таблицей customers
def insert_customer(conn, customer):
    sql = """
        INSERT INTO customers(customer_name, phone_number, email)
        VALUES(?,?,?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, customer)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при вставке клиента: {e}")
        return None

def select_all_customers(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Ошибка при выборке клиентов: {e}")
        return []

def update_customer(conn, customer_id, customer):
    sql = """
        UPDATE customers
        SET customer_name = ?,
            phone_number = ?,
            email = ?
        WHERE id = ?
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (*customer, customer_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении клиента: {e}")

def delete_customer(conn, customer_id):
    sql = "DELETE FROM customers WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (customer_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при удалении клиента: {e}")

# Функции для работы с таблицей rentals
def insert_rental(conn, rental):
    sql = """
        INSERT INTO rentals(bike_id, customer_id, rental_date, return_date, rental_fee, status)
        VALUES(?,?,?,?,?,?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, rental)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при вставке аренды: {e}")
        return None

def select_all_rentals(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rentals")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Ошибка при выборке аренд: {e}")
        return []

def update_rental(conn, rental_id, rental):
    sql = """
        UPDATE rentals
        SET bike_id = ?,
            customer_id = ?,
            rental_date = ?,
            return_date = ?,
            rental_fee = ?,
            status = ?
        WHERE id = ?
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (*rental, rental_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении аренды: {e}")

def delete_rental(conn, rental_id):
    sql = "DELETE FROM rentals WHERE id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (rental_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при удалении аренды: {e}")

def get_rental_summary(conn, date):
    """Получает сводку по арендам за определенную дату."""
    sql = """
        SELECT SUM(rental_fee)
        FROM rentals
        WHERE rental_date = ? AND status = 'Завершено'
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (date,))
        result = cursor.fetchone()[0]
        return result if result else 0  # Возвращает 0, если нет аренд за эту дату
    except sqlite3.Error as e:
        print(f"Ошибка при получении сводки: {e}")
        return 0

def close_connection(conn):
    """Закрывает соединение с базой данных."""
    try:
        if conn:
            conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка при закрытии соединения: {e}")

if __name__ == '__main__':
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()
        print("База данных и таблицы успешно созданы (если их не было).")
    else:
        print("Не удалось создать подключение к базе данных.")