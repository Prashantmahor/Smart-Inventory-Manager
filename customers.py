import psycopg2
from Database import conn


class Customer:

    def create_table():
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id      SERIAL PRIMARY KEY,
                name    VARCHAR(100) NOT NULL,
                contact VARCHAR(100) NOT NULL
            )
        ''')
        conn.commit()
        cur.close()

    def insert_customer(name, contact):
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO customers (name, contact) VALUES (%s, %s)',
            (name, contact)
        )
        conn.commit()
        cur.close()

    def update_customer(customer_id, name=None, contact=None):
        cur = conn.cursor()
        cur.execute('SELECT id FROM customers WHERE id = %s', (customer_id,))
        if not cur.fetchone():
            cur.close()
            return False          # caller handles the message

        # Build query with parameterised values — no f-string injection
        fields, values = [], []
        if name:
            fields.append("name = %s");    values.append(name)
        if contact:
            fields.append("contact = %s"); values.append(contact)

        if not fields:
            cur.close()
            return False

        values.append(customer_id)
        cur.execute(
            f"UPDATE customers SET {', '.join(fields)} WHERE id = %s",
            values
        )
        conn.commit()
        cur.close()
        return True

    def delete_customer(customer_id):
        cur = conn.cursor()
        cur.execute('DELETE FROM customers WHERE id = %s', (customer_id,))
        conn.commit()
        cur.close()

    def get_all_customers():
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers ORDER BY id')
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_customer_by_id(customer_id):
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
        row = cur.fetchone()
        cur.close()
        return row

    def get_sales_by_customer(customer_id):
        cur = conn.cursor()
        cur.execute('''
            SELECT s.id, s.date, s.total_amount
            FROM   sales s
            WHERE  s.customer_id = %s
        ''', (customer_id,))
        rows = cur.fetchall()
        cur.close()
        return rows

    def search_customer(name):
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM customers WHERE name ILIKE %s ORDER BY id',
            ('%' + name + '%',)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
