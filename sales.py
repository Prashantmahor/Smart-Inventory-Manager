import psycopg2
from Database import conn


class Sale:

    def create_table():
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id           SERIAL PRIMARY KEY,
                customer_id  INTEGER        NOT NULL,
                date         DATE           NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        cur.close()

    def insert_sale(customer_id, date, total_amount=0.0):
        """Insert a new sale and return the new sale id."""
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO sales (customer_id, date, total_amount)
               VALUES (%s, %s, %s) RETURNING id''',
            (customer_id, date, total_amount)
        )
        sale_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return sale_id

    def get_all_sales():
        cur = conn.cursor()
        cur.execute('''
            SELECT s.id, c.name, s.date, s.total_amount
            FROM   sales s
            JOIN   customers c ON s.customer_id = c.id
            ORDER  BY s.date DESC
        ''')
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_sale_by_id(sale_id):
        cur = conn.cursor()
        cur.execute('''
            SELECT s.id, c.name, s.date, s.total_amount
            FROM   sales s
            JOIN   customers c ON s.customer_id = c.id
            WHERE  s.id = %s
        ''', (sale_id,))
        row = cur.fetchone()
        cur.close()
        return row

    def finalize_sale(sale_id):
        """Recalculate total from sale_items and persist it."""
        cur = conn.cursor()
        cur.execute(
            'SELECT COALESCE(SUM(quantity * price), 0) FROM sale_items WHERE sale_id = %s',
            (sale_id,)
        )
        total = float(cur.fetchone()[0])
        cur.execute(
            'UPDATE sales SET total_amount = %s WHERE id = %s',
            (total, sale_id)
        )
        conn.commit()
        cur.close()
        return total

    def delete_sale(sale_id):
        cur = conn.cursor()
        # Remove child rows first to avoid FK violation
        cur.execute('DELETE FROM sale_items WHERE sale_id = %s', (sale_id,))
        cur.execute('DELETE FROM sales WHERE id = %s', (sale_id,))
        conn.commit()
        cur.close()

    # ── Analytics ────────────────────────────────────────────────────────── #

    def get_total_sales_by_date(start_date, end_date):
        cur = conn.cursor()
        cur.execute(
            'SELECT COALESCE(SUM(total_amount), 0) FROM sales WHERE date BETWEEN %s AND %s',
            (start_date, end_date)
        )
        result = float(cur.fetchone()[0])
        cur.close()
        return result

    def get_sales_in_range(start_date, end_date):
        cur = conn.cursor()
        cur.execute('''
            SELECT s.id, c.name, s.date, s.total_amount
            FROM   sales s
            JOIN   customers c ON s.customer_id = c.id
            WHERE  s.date BETWEEN %s AND %s
            ORDER  BY s.date DESC
        ''', (start_date, end_date))
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_top_selling_products(limit=10):
        cur = conn.cursor()
        cur.execute('''
            SELECT p.name, SUM(si.quantity) AS total_qty
            FROM   sale_items si
            JOIN   products   p  ON si.product_id = p.id
            GROUP  BY p.id, p.name
            ORDER  BY total_qty DESC
            LIMIT  %s
        ''', (limit,))
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_sales_by_customer(customer_id):
        cur = conn.cursor()
        cur.execute(
            'SELECT id, date, total_amount FROM sales WHERE customer_id = %s ORDER BY date DESC',
            (customer_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_daily_sales_trend():
        cur = conn.cursor()
        cur.execute('''
            SELECT date, SUM(total_amount) AS daily_total
            FROM   sales
            GROUP  BY date
            ORDER  BY date
        ''')
        rows = cur.fetchall()
        cur.close()
        return rows
