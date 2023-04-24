import sqlite3

table_name = 'snake'
table_template = (
    f"""
    CREATE TABLE {table_name} (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        level INTEGER NOT NULL
    );
    """
)

conn = None


def init():
    global tables, conn
    try:
        conn = sqlite3.connect('database.db')

        # create tables
        cur = conn.cursor()
        cur = cur.execute(
            f'SELECT name FROM sqlite_master WHERE name = "{table_name}"')
        isExists = cur.fetchone()

        if not isExists:
            cur.execute(table_template)
            conn.commit()

        cur.close()
        print('Connection succesfully!')
    except Exception as e:
        print('Error with connection!')
        print(str(e))
        exit()


def add_user(data):
    global conn
    try:
        _name = data[0]
        _level = int(data[1])
        query = f"""
            INSERT INTO {table_name} (name, level)
            VALUES('{_name}', {_level}) RETURNING id;
        """
        # get all
        cur = conn.cursor()
        cur.execute(query)
        id = cur.fetchone()[0]
        cur.close()
        conn.commit()
        return id
    except Exception as e:
        print('Error with database!')
        print(str(e))
        exit()


def update_user(id, lvl):
    global conn
    try:
        query = f"""
        UPDATE {table_name}
        set level = {lvl}
        where id = {id};
        """
        # get all
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit()
    except Exception as e:
        print('Error with database!')
        print(str(e))
        exit()


def get_users():
    global conn

    try:
        query = f"SELECT * FROM {table_name}"
        # get all
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        print('fetch')
        if len(data) == 0:
            cur.close()
            return []
        else:
            cur.close()
            return data

    except Exception as e:
        print('Error with database!')
        print(str(e))
        exit()


def close():
    conn.close()
