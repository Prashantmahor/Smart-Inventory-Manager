import psycopg2
import streamlit as st

@st.cache_resource
def get_connection():
    """
    Returns a cached database connection.
    # Reads credentials from st.secrets (secrets.toml on local / Streamlit Cloud secrets).
    """
    try:
        con = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets.get("DB_PORT", "5432"),
            sslmode=st.secrets.get("DB_SSLMODE", "require"),   # required for cloud DBs
        )
        return con
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        st.stop()

  conn = get_connection()


# import psycopg2
# import streamlit as st


# def get_connection():
#     """Create a fresh PostgreSQL connection."""
#     try:
#         return psycopg2.connect(
#             host=st.secrets["DB_HOST"],
#             dbname=st.secrets["DB_NAME"],
#             user=st.secrets["DB_USER"],
#             password=st.secrets["DB_PASSWORD"],
#             port=st.secrets.get("DB_PORT", "5432"),
#             sslmode=st.secrets.get("DB_SSLMODE", "require"),
#             connect_timeout=10,
#         )
#     except Exception as e:
#         st.error(f"Database connection failed: {e}")
#         raise


# def fetch_one(query, params=()):
#     """Execute a SELECT query and return one row."""
#     conn = get_connection()

#     try:
#         with conn.cursor() as cur:
#             cur.execute(query, params)
#             return cur.fetchone()
#     finally:
#         conn.close()


# def fetch_all(query, params=()):
#     """Execute a SELECT query and return all rows."""
#     conn = get_connection()

#     try:
#         with conn.cursor() as cur:
#             cur.execute(query, params)
#             return cur.fetchall()
#     finally:
#         conn.close()


# def execute_query(query, params=()):
#     """Execute INSERT, UPDATE or DELETE queries."""
#     conn = get_connection()

#     try:
#         with conn.cursor() as cur:
#             cur.execute(query, params)

#         conn.commit()

#     except Exception:
#         conn.rollback()
#         raise

#     finally:
#         conn.close()


# def init_db():
#     """Create the required database tables."""
#     conn = get_connection()

#     try:
#         with conn.cursor() as cur:

#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS customers (
#                     customer_id SERIAL PRIMARY KEY,
#                     name VARCHAR(120) NOT NULL,
#                     email VARCHAR(160),
#                     phone VARCHAR(40),
#                     address TEXT,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS products (
#                     product_id SERIAL PRIMARY KEY,
#                     product_name VARCHAR(160) NOT NULL,
#                     category VARCHAR(100),
#                     price NUMERIC(12,2) NOT NULL DEFAULT 0,
#                     stock_quantity INTEGER NOT NULL DEFAULT 0,
#                     reorder_level INTEGER NOT NULL DEFAULT 5,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS sales (
#                     sale_id SERIAL PRIMARY KEY,
#                     customer_id INTEGER
#                         REFERENCES customers(customer_id)
#                         ON DELETE SET NULL,
#                     sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     total_amount NUMERIC(12,2) NOT NULL DEFAULT 0
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS sales_items (
#                     sale_item_id SERIAL PRIMARY KEY,
#                     sale_id INTEGER NOT NULL
#                         REFERENCES sales(sale_id)
#                         ON DELETE CASCADE,
#                     product_id INTEGER NOT NULL
#                         REFERENCES products(product_id),
#                     quantity INTEGER NOT NULL,
#                     unit_price NUMERIC(12,2) NOT NULL,
#                     subtotal NUMERIC(12,2) NOT NULL
#                 );
#             """)

#         conn.commit()

#     except Exception:
#         conn.rollback()
#         raise

#     finally:
#         conn.close()
