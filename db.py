import psycopg2
import os

# Use Render's DATABASE_URL environment variable
DB_NAME = os.environ.get('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DB_NAME, sslmode='require')




def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS routine (
            id SERIAL PRIMARY KEY,
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
            c.execute('INSERT INTO routine (day, "1st Period", "2nd Period", "3rd Period", lab) VALUES (%s, %s, %s, %s, %s)',
                      (day, '', '', '', ''))
    conn.commit()

    c.execute('''
        CREATE TABLE IF NOT EXISTS table_title (
            title TEXT
        )
    ''')
    c.execute("INSERT INTO table_title (title) VALUES ('CLASS TESTS & LABS')")
    conn.commit()

    conn.close()


def get_title():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT title FROM table_title LIMIT 1')
    result = c.fetchone()
    conn.close()
    return result[0] if result else ''


def get_routine():
    conn = get_connection()
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
    if not routine_data['routine']:
        return

    # Get column names dynamically from the first row
    column_names = list(routine_data['routine'][0].keys())

    # Prepare SQL-compatible column names (sanitize if needed)
    columns_sql = ', '.join([f'"{col}" TEXT' for col in column_names])

    conn = get_connection()
    c = conn.cursor()

    # Drop and recreate the table dynamically
    c.execute('DROP TABLE IF EXISTS routine')
    c.execute(f'''
        CREATE TABLE routine (
            id SERIAL PRIMARY KEY,
            {columns_sql}
        )
    ''')
    # Insert the new data
    for row in routine_data['routine']:
        placeholders = ', '.join(['%s'] * len(column_names))
        values = [row.get(col, '') for col in column_names]
        c.execute(f'''
            INSERT INTO routine ({', '.join(['"' + col + '"' for col in column_names])})
            VALUES ({placeholders})
        ''', values)

    conn.commit()
    c.execute('DROP TABLE IF EXISTS table_title')  # Clear existing title
    c.execute('''
            CREATE TABLE table_title (
                title TEXT
            )
        ''')
    c.execute('INSERT INTO table_title (title) VALUES (%s)', (routine_data['title'],))
    conn.commit()

    conn.close()
