# Smart Inventory & Billing System 🏪

A full-featured inventory and billing web app built with **Streamlit** + **PostgreSQL**.

---

## Features
| Module | What you can do |
|---|---|
| Dashboard | KPIs, recent sales, low-stock alerts |
| Customers | Add / Edit / Delete / Search |
| Products | Add / Edit / Delete, colour-coded stock levels |
| Sales | Create sale → add items → auto-total → receipt |
| Analytics | Date-range reports, top products, customer history |

---

## Local Setup (5 minutes)

### 1. Clone / copy the project
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database connection
Edit `.streamlit/secrets.toml`:
```toml
DB_HOST     = "localhost"
DB_NAME     = "ecommerce"
DB_USER     = "postgres"
DB_PASSWORD = "your_password"
DB_PORT     = "5432"
DB_SSLMODE  = "disable"
```

### 5. Run the app
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

---

## Deploy to Streamlit Cloud (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```
> ⚠️ `.streamlit/secrets.toml` is in `.gitignore` — it will NOT be pushed.

### Step 2 — Get a cloud PostgreSQL database (free options)
| Provider | Free tier | SSL |
|---|---|---|
| [Supabase](https://supabase.com) | 500 MB | Required |
| [Neon](https://neon.tech) | 3 GB | Required |
| [Railway](https://railway.app) | 100 MB | Required |
| [ElephantSQL](https://www.elephantsql.com) | 20 MB | Optional |

After creating your DB, copy the **host, database, user, password, port** values.

### Step 3 — Deploy on Streamlit Cloud
1. Go to **https://share.streamlit.io** → Sign in with GitHub
2. Click **New app**
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`
4. Click **Advanced settings → Secrets** and paste:

```toml
DB_HOST     = "your-cloud-db-host"
DB_NAME     = "your_db_name"
DB_USER     = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_PORT     = "5432"
DB_SSLMODE  = "require"
```

5. Click **Deploy!** — your app will be live in ~60 seconds.

---

## Project Structure
```
├── app.py              ← Streamlit UI (main entry point)
├── Database.py         ← Connection pool via st.cache_resource
├── customers.py        ← Customer CRUD
├── products.py         ← Product CRUD
├── sales.py            ← Sale operations + analytics
├── sales_items.py      ← Line-item operations
├── requirements.txt
├── .gitignore
└── .streamlit/
    ├── secrets.toml    ← DB credentials (local only, not in Git)
    └── config.toml     ← Theme and server settings
```

---

## Common Issues

| Problem | Fix |
|---|---|
| `connection failed` | Check secrets.toml credentials and that Postgres is running |
| `SSL required` | Set `DB_SSLMODE = "require"` for cloud DBs |
| Tables not created | The app auto-creates tables on first load via `CREATE TABLE IF NOT EXISTS` |
| `psycopg2` error on M1 Mac | Use `pip install psycopg2-binary` (already in requirements.txt) |
