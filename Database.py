import psycopg2
import streamlit as st

@st.cache_resource
def get_connection():
    """
    Returns a cached database connection.
    Reads credentials from st.secrets (secrets.toml on local / Streamlit Cloud secrets).
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
