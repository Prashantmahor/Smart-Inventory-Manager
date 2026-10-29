import psycopg2
from Database import conn


class Product:

    def create_table():
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id          SERIAL PRIMARY KEY,
                name        VARCHAR(100) NOT NULL,
                description TEXT,
                price       DECIMAL(10, 2) NOT NULL,
                quantity    INTEGER NOT NULL
            )
        ''')
        conn.commit()
        cur.close()

    def insert_product(name, description, price, quantity):
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO products (name, description, price, quantity)
               VALUES (%s, %s, %s, %s)''',
            (name, description, price, quantity)
        )
        conn.commit()
        cur.close()

    def update_product(product_id, name=None, description=None,
                       price=None, quantity=None):
        cur = conn.cursor()
        cur.execute('SELECT id FROM products WHERE id = %s', (product_id,))
        if not cur.fetchone():
            cur.close()
            return False

        fields, values = [], []
        if name        is not None: fields.append("name = %s");        values.append(name)
        if description is not None: fields.append("description = %s"); values.append(description)
        if price       is not None: fields.append("price = %s");       values.append(price)
        if quantity    is not None: fields.append("quantity = %s");     values.append(quantity)

        if not fields:
            cur.close()
            return False

        values.append(product_id)
        cur.execute(
            f"UPDATE products SET {', '.join(fields)} WHERE id = %s",
            values
        )
        conn.commit()
        cur.close()
        return True

    def delete_product(product_id):
        cur = conn.cursor()
        cur.execute('DELETE FROM products WHERE id = %s', (product_id,))
        conn.commit()
        cur.close()

    def view_products():
        cur = conn.cursor()
        cur.execute('SELECT * FROM products ORDER BY id')
        rows = cur.fetchall()
        cur.close()
        return rows

    def view_product_id(product_id):
        cur = conn.cursor()
        cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        row = cur.fetchone()
        cur.close()
        return row

    def search_products(keyword):
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM products WHERE name ILIKE %s ORDER BY id',
            ('%' + keyword + '%',)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

# from Database import get_connection


# class Product:

#     @staticmethod
#     def create_table():
#         conn = get_connection()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     CREATE TABLE IF NOT EXISTS products (
#                         id SERIAL PRIMARY KEY,
#                         name VARCHAR(100) NOT NULL,
#                         description TEXT,
#                         price DECIMAL(10, 2) NOT NULL,
#                         quantity INTEGER NOT NULL
#                     )
#                 """)
#             conn.commit()
#         except Exception:
#             conn.rollback()
#             raise
#         finally:
#             conn.close()

#     @staticmethod
#     def insert_product(name, description, price, quantity):
#         conn = get_connection()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     INSERT INTO products (name, description, price, quantity)
#                     VALUES (%s, %s, %s, %s)
#                 """, (name, description, price, quantity))
#             conn.commit()
#         except Exception:
#             conn.rollback()
#             raise
#         finally:
#             conn.close()

#     @staticmethod
#     def update_product(
#         product_id,
#         name=None,
#         description=None,
#         price=None,
#         quantity=None
#     ):
#         conn = get_connection()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT id FROM products WHERE id = %s",
#                     (product_id,)
#                 )

#                 if not cur.fetchone():
#                     return False

#                 fields = []
#                 values = []

#                 if name is not None:
#                     fields.append("name = %s")
#                     values.append(name)

#                 if description is not None:
#                     fields.append("description = %s")
#                     values.append(description)

#                 if price is not None:
#                     fields.append("price = %s")
#                     values.append(price)

#                 if quantity is not None:
#                     fields.append("quantity = %s")
#                     values.append(quantity)

#                 if not fields:
#                     return False

#                 values.append(product_id)

#                 query = f"""
#                     UPDATE products
#                     SET {', '.join(fields)}
#                     WHERE id = %s
#                 """

#                 cur.execute(query, values)

#             conn.commit()
#             return True

#         except Exception:
#             conn.rollback()
#             raise
#         finally:
#             conn.close()

#     @staticmethod
#     def delete_product(product_id):
#         conn = get_connection()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "DELETE FROM products WHERE id = %s",
#                     (product_id,)
#                 )
#                 deleted = cur.rowcount > 0

#             conn.commit()
#             return deleted

#         except Exception:
#             conn.rollback()
#             raise
#         finally:
#             conn.close()

#     @staticmethod
#     def get_all_products():
#         conn = get_connection()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT * FROM products ORDER BY id")
#                 return cur.fetchall()
#         finally:
#             conn.close()

#     @staticmethod
#     def get_product_by_id(product_id):
#         conn = get_connection()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT * FROM products WHERE id = %s",
#                     (product_id,)
#                 )
#                 return cur.fetchone()
#         finally:
#             conn.close()

#     @staticmethod
#     def search_product(name):
#         conn = get_connection()
#         try:
#             with conn.cursor() as cur:
#                 cur.execute("""
#                     SELECT *
#                     FROM products
#                     WHERE name ILIKE %s
#                     ORDER BY id
#                 """, ('%' + name + '%',))
#                 return cur.fetchall()
#         finally:
#             conn.close()
