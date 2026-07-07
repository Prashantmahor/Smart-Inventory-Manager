# 📦 Smart Inventory Management System

A Smart Inventory Management System developed using **Python**, **PostgreSQL**, and **SQL** to efficiently manage customers, products, inventory, sales, and billing. The system automates inventory operations, tracks customer purchases, generates sales records, and provides analytical reports for better business decision-making.

---

# 📖 Problem Statement

Small and medium-sized businesses often manage inventory and sales manually, which can lead to:

- Inaccurate inventory records
- Duplicate customer information
- Billing errors
- Difficulty tracking sales history
- Poor stock management
- Time-consuming report generation

This project provides a centralized inventory management solution that automates these operations using a relational database.

---

# 🎯 Objectives

- Manage customer information
- Manage product inventory
- Generate sales and bills
- Track inventory stock
- Store complete sales history
- Generate sales reports
- Reduce manual work and human errors

---

# 🚀 Features

## Customer Management
- Add new customers
- Update customer information
- Delete customers
- Search customers
- View all customers
- View customer purchase history

## Product Management
- Add products
- Update products
- Delete products
- View available inventory
- Search products

## Sales Management
- Create sales records
- Store purchased products
- Generate bills
- Calculate total sales
- View sales history

## Inventory Management
- Maintain product stock
- Track available quantity
- Update inventory after modifications

## Reports & Analytics
- Total Sales
- Customer Purchase History
- Top Selling Products
- Sales Between Dates
- Product-wise Sales Reports

---

# 🛠 Technologies Used

- Python
- PostgreSQL
- SQL
- psycopg2
- Streamlit (UI, if applicable)
- Git & GitHub

---

# 📂 Project Structure

```text
Smart-Inventory-System/
│
├── app.py
├── Database.py
├── customers.py
├── products.py
├── sales.py
├── sales_items.py
├── requirements.txt
├── README.md
└── database.sql
```

---

# 🗄 Database Schema

## Customers

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| name | VARCHAR |
| contact | VARCHAR |

---

## Products

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| name | VARCHAR |
| description | TEXT |
| price | DECIMAL |
| quantity | INTEGER |

---

## Sales

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| customer_id | INTEGER |
| date | DATE |
| total_amount | DECIMAL |

---

## Sale_Items

| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| sale_id | INTEGER |
| product_id | INTEGER |
| quantity | INTEGER |
| price | DECIMAL |

---

# 🧩 Database Relationships

Customers (1) ------ (Many) Sales

Sales (1) ---------- (Many) Sale_Items

Products (1) ------- (Many) Sale_Items

---

# 🔄 Project Workflow

1. Add Customer
2. Add Products
3. Create Sale
4. Select Customer
5. Select Products
6. Generate Bill
7. Store Sale Details
8. Update Inventory
9. Generate Reports

---

# 📊 SQL Concepts Used

- CREATE TABLE
- INSERT
- SELECT
- UPDATE
- DELETE
- WHERE
- ORDER BY
- GROUP BY
- HAVING
- Aggregate Functions
- INNER JOIN
- Foreign Keys
- Primary Keys

---

# 📈 Reports Generated

- Customer Purchase History
- Product Sales Report
- Top Selling Products
- Total Revenue
- Sales Summary

---

# 🔐 Future Improvements

- User Authentication
- Role-Based Access Control
- Barcode Scanner Integration
- Invoice PDF Generation
- Dashboard with Charts
- Email Notifications
- Low Stock Alerts
- Export Reports to Excel/PDF
- Cloud Database Integration
- REST API Support

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Smart-Inventory-System.git
```

## Navigate

```bash
cd Smart-Inventory-System
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure PostgreSQL

Create a PostgreSQL database and update your database credentials inside `Database.py`.

## Run Application

```bash
python app.py
```

or

```bash
streamlit run app.py
```

(depending on your application)

---

# 📷 Screenshots

Add screenshots here.

Example:

- Login Page
- Dashboard
- Customer Module
- Product Module
- Billing Module
- Sales Report

---

# 💡 Learning Outcomes

Through this project, I gained practical experience in:

- Database Design
- SQL Query Writing
- CRUD Operations
- Relational Database Management
- PostgreSQL Integration with Python
- Inventory Management Logic
- Sales Analytics
- Data Modeling

---

# 👨‍💻 Author

**Prashant Kumar**

Computer Science & Engineering (Cyber Security)

Python | SQL | PostgreSQL | Data Analytics | MERN Stack

---

# ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.
