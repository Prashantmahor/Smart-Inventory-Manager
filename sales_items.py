import psycopg2
from Database import conn


class SaleItem:

    def create_table():
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id         SERIAL PRIMARY KEY,
                sale_id    INTEGER        NOT NULL REFERENCES sales(id)    ON DELETE CASCADE,
                product_id INTEGER        NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
                quantity   INTEGER        NOT NULL,
                price      DECIMAL(10, 2) NOT NULL
            )
        ''')
        conn.commit()
        cur.close()

    def add_item(sale_id, product_id, quantity, price):
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO sale_items (sale_id, product_id, quantity, price)
               VALUES (%s, %s, %s, %s)''',
            (sale_id, product_id, quantity, price)
        )
        conn.commit()
        cur.close()

    def get_items_by_sale(sale_id):
        cur = conn.cursor()
        cur.execute('''
            SELECT si.id, p.name, si.quantity, si.price,
                   (si.quantity * si.price) AS line_total
            FROM   sale_items si
            JOIN   products   p ON si.product_id = p.id
            WHERE  si.sale_id = %s
        ''', (sale_id,))
        rows = cur.fetchall()
        cur.close()
        return rows

    def delete_item(item_id):
        cur = conn.cursor()
        cur.execute('DELETE FROM sale_items WHERE id = %s', (item_id,))
        conn.commit()
        cur.close()
