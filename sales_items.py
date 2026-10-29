# import psycopg2
# from Database import conn


# class SaleItem:

#     def create_table():
#         cur = conn.cursor()
#         cur.execute('''
#             CREATE TABLE IF NOT EXISTS sale_items (
#                 id         SERIAL PRIMARY KEY,
#                 sale_id    INTEGER        NOT NULL REFERENCES sales(id)    ON DELETE CASCADE,
#                 product_id INTEGER        NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
#                 quantity   INTEGER        NOT NULL,
#                 price      DECIMAL(10, 2) NOT NULL
#             )
#         ''')
#         conn.commit()
#         cur.close()

#     def add_item(sale_id, product_id, quantity, price):
#         cur = conn.cursor()
#         cur.execute(
#             '''INSERT INTO sale_items (sale_id, product_id, quantity, price)
#                VALUES (%s, %s, %s, %s)''',
#             (sale_id, product_id, quantity, price)
#         )
#         conn.commit()
#         cur.close()

#     def get_items_by_sale(sale_id):
#         cur = conn.cursor()
#         cur.execute('''
#             SELECT si.id, p.name, si.quantity, si.price,
#                    (si.quantity * si.price) AS line_total
#             FROM   sale_items si
#             JOIN   products   p ON si.product_id = p.id
#             WHERE  si.sale_id = %s
#         ''', (sale_id,))
#         rows = cur.fetchall()
#         cur.close()
#         return rows

#     def delete_item(item_id):
#         cur = conn.cursor()
#         cur.execute('DELETE FROM sale_items WHERE id = %s', (item_id,))
#         conn.commit()
#         cur.close()

from Database import get_connection


class SaleItem:

    @staticmethod
    def create_table():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sale_items (
                        id SERIAL PRIMARY KEY,
                        sale_id INTEGER NOT NULL
                            REFERENCES sales(id) ON DELETE CASCADE,
                        product_id INTEGER NOT NULL
                            REFERENCES products(id) ON DELETE RESTRICT,
                        quantity INTEGER NOT NULL,
                        price DECIMAL(10, 2) NOT NULL
                    )
                """)
            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def add_item(sale_id, product_id, quantity, price):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO sale_items
                        (sale_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """, (sale_id, product_id, quantity, price))

            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def get_items_by_sale(sale_id):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        si.id,
                        p.name,
                        si.quantity,
                        si.price,
                        (si.quantity * si.price) AS line_total
                    FROM sale_items si
                    JOIN products p ON si.product_id = p.id
                    WHERE si.sale_id = %s
                    ORDER BY si.id
                """, (sale_id,))

                return cur.fetchall()

        finally:
            conn.close()

    @staticmethod
    def delete_item(item_id):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM sale_items WHERE id = %s",
                    (item_id,)
                )
                deleted = cur.rowcount > 0

            conn.commit()
            return deleted

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def get_all_items():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        si.id,
                        si.sale_id,
                        p.name,
                        si.quantity,
                        si.price,
                        (si.quantity * si.price) AS line_total
                    FROM sale_items si
                    JOIN products p ON si.product_id = p.id
                    ORDER BY si.id
                """)

                return cur.fetchall()

        finally:
            conn.close()
