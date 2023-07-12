import sqlite3

def create_product_table():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                product_name TEXT,
                price FLOAT
            )
        ''')

def create_task_table():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                total_rows,
                is_completed BOOLEAN DEFAULT FALSE,
                records_created INTEGER DEFAULT 0,
                records_updated INTEGER DEFAULT 0,
                rows_with_errors TEXT
            )
        ''')

def get_all_data():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        data = cursor.execute('''
            SELECT * FROM products;
        ''').fetchall()
        return data


def get_last_id():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        max_id = cursor.execute('''
            SELECT MAX(ID) FROM products;
        ''').fetchone()[0]
        return max_id

def insert_task(task_data):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (task_name, total_rows)
            VALUES (?, ?)
        ''', (task_data['name'], task_data['total_rows']))
        return cursor.lastrowid

def insert_product(product_data):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO products (id, product_name, price)
            VALUES (?, ?, ?)
        ''', (product_data['id'], product_data['name'], product_data['price']))

def get_task_info(task_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        data = cursor.execute('''
            SELECT * FROM tasks
            WHERE id = (?)
        ''', (task_id,))
        return data.fetchone()

def update_task(task_data):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks
            SET is_completed = ?,
                records_created = ?,
                records_updated = ?
            WHERE id = ?
        ''', (
            task_data['is_completed'],
            task_data['records_created'],
            task_data['records_updated'],
            task_data['id'],
        ))