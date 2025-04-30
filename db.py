import sqlite3

DB_NAME = 'app.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS routine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Day TEXT,
            "1st Period" TEXT,
            "2nd Period" TEXT,
            "3rd Period" TEXT,
            Lab TEXT
        )
    ''')
    # Check if empty and pre-fill default rows
    c.execute('SELECT COUNT(*) FROM routine')
    if c.fetchone()[0] == 0:
        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday']
        for day in days:
            c.execute('INSERT INTO routine (day, "1st Period", "2nd Period", "3rd Period", lab) VALUES (?, ?, ?, ?, ?)',
                      (day, '', '', '', ''))
    conn.commit()
    conn.close()


def get_routine():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM routine')
    rows = c.fetchall()
    # Get column names dynamically
    columns = [description[0] for description in c.description]
    conn.close()

    # Convert rows to dictionaries, using column names as keys
    routine_data = [dict(zip(columns, row)) for row in rows]
    return routine_data


def save_routine(routine_data):
    if not routine_data:
        return

    # Get column names dynamically from the first row
    column_names = list(routine_data[0].keys())

    # Prepare SQL-compatible column names (sanitize if needed)
    columns_sql = ', '.join([f'"{col}" TEXT' for col in column_names])

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Drop and recreate the table dynamically
    c.execute('DROP TABLE IF EXISTS routine')
    c.execute(f'''
        CREATE TABLE routine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns_sql}
        )
    ''')
    # Insert the new data
    for row in routine_data:
        placeholders = ', '.join(['?'] * len(column_names))
        values = [row.get(col, '') for col in column_names]
        c.execute(f'''
            INSERT INTO routine ({', '.join(['"' + col + '"' for col in column_names])})
            VALUES ({placeholders})
        ''', values)

    conn.commit()
    conn.close()
