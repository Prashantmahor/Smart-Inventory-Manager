"""
Smart Inventory & Billing System
Streamlit front-end — deployment-ready
"""
import pandas as pd
from datetime import date

from Database import get_connection,conn
from customers import Customer
from products import Product
from sales import Sale
from sales_items import SaleItem

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Inventory & Billing",
    page_icon="🏪",
    layout="wide",
)

# ── Table bootstrap (runs once per session) ───────────────────────────────────
def initialize_tables():
    try:
        Customer.create_table()
        Product.create_table()
        Sale.create_table()
        SaleItem.create_table()
    except Exception as e:
        st.error(f"Table initialisation error: {e}")
        st.stop()

if "tables_ready" not in st.session_state:
    initialize_tables()
    st.session_state.tables_ready = True

# ── Sidebar navigation ────────────────────────────────────────────────────────
st.sidebar.title("🏪 Inventory & Billing")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "👥 Customers", "📦 Products", "💰 Sales", "📈 Analytics"],
)
st.sidebar.markdown("---")
st.sidebar.caption("Smart Inventory & Billing System v1.0")


# ══════════════════════════════════════════════════════════════════════════════
# 1. DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Welcome to the **Smart Inventory & Billing System**.")
    st.markdown("---")

    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customers")
        c_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM products")
        p_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*), COALESCE(SUM(total_amount),0) FROM sales")
        s_count, s_total = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM products WHERE quantity < 10")
        low_stock = cur.fetchone()[0]
        cur.close()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Customers",    c_count)
        col2.metric("📦 Products",     p_count)
        col3.metric("💰 Total Sales",  s_count)
        col4.metric("💵 Total Revenue", f"${float(s_total):,.2f}")

        if low_stock:
            st.warning(f"⚠️  {low_stock} product(s) with stock below 10 units.")

        # Recent sales table
        st.markdown("### Recent Sales")
        recent = Sale.get_all_sales()
        if recent:
            df = pd.DataFrame(recent, columns=["Sale ID", "Customer", "Date", "Amount ($)"])
            df["Amount ($)"] = df["Amount ($)"].apply(lambda x: f"${float(x):,.2f}")
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        else:
            st.info("No sales recorded yet.")

    except Exception as e:
        st.error(f"Dashboard error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 2. CUSTOMERS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 Customers":
    st.title("👥 Customer Management")
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["View All", "Add", "Edit", "Delete", "Search"]
    )

    # ── View All ──────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("All Customers")
        rows = Customer.get_all_customers()
        if rows:
            df = pd.DataFrame(rows, columns=["ID", "Name", "Contact"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No customers yet.")

    # ── Add ───────────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("Add New Customer")
        with st.form("add_cust_form", clear_on_submit=True):
            name    = st.text_input("Name *")
            contact = st.text_input("Contact (phone / email) *")
            if st.form_submit_button("➕ Add Customer"):
                if name.strip() and contact.strip():
                    try:
                        Customer.insert_customer(name.strip(), contact.strip())
                        st.success(f"Customer **{name}** added!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Both fields are required.")

    # ── Edit ──────────────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Edit Customer")
        rows = Customer.get_all_customers()
        if rows:
            opts = {f"{r[1]} (ID {r[0]})": r[0] for r in rows}
            sel  = st.selectbox("Select customer", list(opts.keys()), key="edit_cust_sel")
            cid  = opts[sel]
            cust = Customer.get_customer_by_id(cid)

            with st.form("edit_cust_form"):
                new_name    = st.text_input("Name",    value=cust[1])
                new_contact = st.text_input("Contact", value=cust[2])
                if st.form_submit_button("💾 Save Changes"):
                    try:
                        Customer.update_customer(cid, new_name.strip(), new_contact.strip())
                        st.success("Customer updated!")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("No customers to edit.")

    # ── Delete ────────────────────────────────────────────────────────────────
    with tab4:
        st.subheader("Delete Customer")
        rows = Customer.get_all_customers()
        if rows:
            opts = {f"{r[1]} (ID {r[0]})": r[0] for r in rows}
            sel  = st.selectbox("Select customer", list(opts.keys()), key="del_cust_sel")
            st.warning("⚠️ Deleting a customer removes their record. Sales history remains.")
            if st.button("🗑️ Delete Customer", type="primary"):
                try:
                    Customer.delete_customer(opts[sel])
                    st.success("Customer deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("No customers to delete.")

    # ── Search ────────────────────────────────────────────────────────────────
    with tab5:
        st.subheader("Search Customers")
        keyword = st.text_input("Enter name to search")
        if keyword:
            results = Customer.search_customer(keyword)
            if results:
                df = pd.DataFrame(results, columns=["ID", "Name", "Contact"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No matching customers found.")


# ══════════════════════════════════════════════════════════════════════════════
# 3. PRODUCTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📦 Products":
    st.title("📦 Product Management")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add", "Edit", "Delete"])

    # ── View All ──────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("All Products")
        rows = Product.view_products()
        if rows:
            df = pd.DataFrame(rows, columns=["ID", "Name", "Description", "Price ($)", "Stock"])
            df["Price ($)"] = df["Price ($)"].apply(lambda x: f"${float(x):,.2f}")
            # Highlight low stock
            def _stock_color(val):
                color = "red" if int(val) < 10 else "green"
                return f"color: {color}; font-weight: bold"
            st.dataframe(
                df.style.applymap(_stock_color, subset=["Stock"]),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No products yet.")

    # ── Add ───────────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("Add New Product")
        with st.form("add_prod_form", clear_on_submit=True):
            name  = st.text_input("Product Name *")
            desc  = st.text_area("Description")
            price = st.number_input("Price ($)", min_value=0.0, step=0.01, format="%.2f")
            qty   = st.number_input("Initial Stock", min_value=0, step=1)
            if st.form_submit_button("➕ Add Product"):
                if name.strip():
                    try:
                        Product.insert_product(name.strip(), desc, price, qty)
                        st.success(f"Product **{name}** added!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Product name is required.")

    # ── Edit ──────────────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Edit Product")
        rows = Product.view_products()
        if rows:
            opts = {f"{r[1]} (ID {r[0]})": r[0] for r in rows}
            sel  = st.selectbox("Select product", list(opts.keys()), key="edit_prod_sel")
            pid  = opts[sel]
            prod = Product.view_product_id(pid)

            with st.form("edit_prod_form"):
                new_name  = st.text_input("Name",        value=prod[1])
                new_desc  = st.text_area("Description",  value=prod[2] or "")
                new_price = st.number_input("Price ($)", value=float(prod[3]), min_value=0.0, step=0.01, format="%.2f")
                new_qty   = st.number_input("Stock",     value=int(prod[4]),   min_value=0,   step=1)
                if st.form_submit_button("💾 Save Changes"):
                    try:
                        Product.update_product(pid, new_name, new_desc, new_price, new_qty)
                        st.success("Product updated!")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("No products to edit.")

    # ── Delete ────────────────────────────────────────────────────────────────
    with tab4:
        st.subheader("Delete Product")
        rows = Product.view_products()
        if rows:
            opts = {f"{r[1]} (ID {r[0]})": r[0] for r in rows}
            sel  = st.selectbox("Select product", list(opts.keys()), key="del_prod_sel")
            st.warning("⚠️ Cannot delete a product that is part of existing sale items.")
            if st.button("🗑️ Delete Product", type="primary"):
                try:
                    Product.delete_product(opts[sel])
                    st.success("Product deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("No products to delete.")


# ══════════════════════════════════════════════════════════════════════════════
# 4. SALES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰 Sales":
    st.title("💰 Sales Management")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Create Sale", "View Sales", "Generate Bill"])

    # ── Create Sale ───────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Create New Sale")

        customers = Customer.get_all_customers()
        products  = Product.view_products()

        if not customers:
            st.info("Add customers first.")
        elif not products:
            st.info("Add products first.")
        else:
            # Step 1 – choose customer & date
            cust_opts = {f"{r[1]} (ID {r[0]})": r[0] for r in customers}
            sel_cust  = st.selectbox("Customer", list(cust_opts.keys()))
            sale_date = st.date_input("Sale Date", value=date.today())

            if st.button("🛒 Start Sale"):
                try:
                    sid = Sale.insert_sale(cust_opts[sel_cust], sale_date, 0.0)
                    st.session_state["active_sale_id"] = sid
                    st.session_state["sale_items"]     = []
                    st.success(f"Sale #{sid} created. Add items below.")
                except Exception as e:
                    st.error(f"Error: {e}")

            # Step 2 – add items
            if "active_sale_id" in st.session_state:
                sid = st.session_state["active_sale_id"]
                st.markdown(f"**Adding items to Sale #{sid}**")

                prod_opts = {f"{r[1]} (ID {r[0]}) — Stock: {r[4]}": r for r in products}
                sel_prod  = st.selectbox("Product", list(prod_opts.keys()))
                prod_row  = prod_opts[sel_prod]

                col1, col2 = st.columns(2)
                with col1:
                    qty   = st.number_input("Quantity", min_value=1, max_value=int(prod_row[4]), step=1)
                with col2:
                    price = st.number_input("Unit Price ($)", value=float(prod_row[3]), min_value=0.0, step=0.01, format="%.2f")

                if st.button("➕ Add Item"):
                    if qty > prod_row[4]:
                        st.error("Not enough stock.")
                    else:
                        try:
                            SaleItem.add_item(sid, prod_row[0], qty, price)
                            # Decrement stock
                            Product.update_product(prod_row[0], quantity=prod_row[4] - qty)
                            st.success(f"Added {qty}× {prod_row[1]}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

                # Show items added so far
                items = SaleItem.get_items_by_sale(sid)
                if items:
                    st.markdown("**Items in this sale:**")
                    idf = pd.DataFrame(items, columns=["Item ID", "Product", "Qty", "Unit Price", "Line Total"])
                    idf["Unit Price"] = idf["Unit Price"].apply(lambda x: f"${float(x):,.2f}")
                    idf["Line Total"] = idf["Line Total"].apply(lambda x: f"${float(x):,.2f}")
                    st.dataframe(idf, use_container_width=True, hide_index=True)
                    running_total = sum(float(r[4]) for r in items)
                    st.markdown(f"**Running Total: ${running_total:,.2f}**")

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Finish & Save Sale", type="primary"):
                        try:
                            total = Sale.finalize_sale(sid)
                            st.success(f"Sale #{sid} finalised! Total: **${total:,.2f}**")
                            del st.session_state["active_sale_id"]
                            del st.session_state["sale_items"]
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                with col_b:
                    if st.button("❌ Cancel Sale"):
                        try:
                            Sale.delete_sale(sid)
                            del st.session_state["active_sale_id"]
                            st.warning("Sale cancelled and removed.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

    # ── View Sales ────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("All Sales")
        rows = Sale.get_all_sales()
        if rows:
            df = pd.DataFrame(rows, columns=["Sale ID", "Customer", "Date", "Total ($)"])
            df["Total ($)"] = df["Total ($)"].apply(lambda x: f"${float(x):,.2f}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No sales yet.")

    # ── Generate Bill ─────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Generate Bill / Receipt")
        rows = Sale.get_all_sales()
        if rows:
            sale_opts = {f"Sale #{r[0]} — {r[1]} ({r[2]})": r[0] for r in rows}
            sel_sale  = st.selectbox("Select Sale", list(sale_opts.keys()))
            sid       = sale_opts[sel_sale]

            if st.button("🖨️ Generate Bill"):
                sale  = Sale.get_sale_by_id(sid)
                items = SaleItem.get_items_by_sale(sid)

                st.markdown("---")
                st.markdown("## 🧾 RECEIPT")
                col1, col2 = st.columns(2)
                col1.markdown(f"**Sale ID:** {sale[0]}")
                col1.markdown(f"**Customer:** {sale[1]}")
                col2.markdown(f"**Date:** {sale[2]}")
                st.markdown("---")

                if items:
                    idf = pd.DataFrame(items, columns=["#", "Product", "Qty", "Unit Price ($)", "Line Total ($)"])
                    idf["Unit Price ($)"] = idf["Unit Price ($)"].apply(lambda x: f"${float(x):,.2f}")
                    idf["Line Total ($)"] = idf["Line Total ($)"].apply(lambda x: f"${float(x):,.2f}")
                    idf = idf.drop(columns=["#"])
                    st.dataframe(idf, use_container_width=True, hide_index=True)
                    st.markdown("---")
                    grand_total = sum(float(r[4]) for r in items)
                    st.markdown(f"### 💵 Grand Total: **${grand_total:,.2f}**")
                else:
                    st.info("No items found for this sale.")
        else:
            st.info("No sales to bill yet.")


# ══════════════════════════════════════════════════════════════════════════════
# 5. ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Analytics":
    st.title("📈 Analytics & Reports")
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Sales Summary", "Date Range", "Top Products",
        "Low Stock", "Customer History"
    ])

    # ── Sales Summary ─────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Sales Summary")
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*), COALESCE(SUM(total_amount),0) FROM sales")
            s_count, s_total = cur.fetchone()
            cur.close()

            col1, col2 = st.columns(2)
            col1.metric("Total Transactions", s_count)
            col2.metric("Total Revenue",      f"${float(s_total):,.2f}")

            trend = Sale.get_daily_sales_trend()
            if trend:
                df = pd.DataFrame(trend, columns=["Date", "Revenue"])
                df["Date"]    = df["Date"].astype(str)
                df["Revenue"] = df["Revenue"].astype(float)
                df = df.set_index("Date")
                st.markdown("### Daily Revenue Trend")
                st.line_chart(df)
            else:
                st.info("No sales data for chart.")
        except Exception as e:
            st.error(f"Error: {e}")

    # ── Date Range ────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("Sales by Date Range")
        col1, col2 = st.columns(2)
        start = col1.date_input("From", value=date.today().replace(day=1))
        end   = col2.date_input("To",   value=date.today())

        if st.button("🔍 Run Report"):
            if start > end:
                st.warning("Start date must be before end date.")
            else:
                rows  = Sale.get_sales_in_range(start, end)
                total = Sale.get_total_sales_by_date(start, end)
                if rows:
                    df = pd.DataFrame(rows, columns=["Sale ID", "Customer", "Date", "Amount ($)"])
                    df["Amount ($)"] = df["Amount ($)"].apply(lambda x: f"${float(x):,.2f}")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.metric("Period Revenue", f"${total:,.2f}")
                else:
                    st.info("No sales in this period.")

    # ── Top Products ──────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Top Selling Products")
        rows = Sale.get_top_selling_products(limit=10)
        if rows:
            df = pd.DataFrame(rows, columns=["Product", "Units Sold"])
            df["Units Sold"] = df["Units Sold"].astype(int)
            col1, col2 = st.columns([1, 2])
            col1.dataframe(df, use_container_width=True, hide_index=True)
            col2.bar_chart(df.set_index("Product"))
        else:
            st.info("No sales data yet.")

    # ── Low Stock ─────────────────────────────────────────────────────────────
    with tab4:
        st.subheader("Low Stock Alert (< 10 units)")
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT name, quantity FROM products WHERE quantity < 10 ORDER BY quantity ASC"
            )
            rows = cur.fetchall()
            cur.close()

            if rows:
                df = pd.DataFrame(rows, columns=["Product", "Stock"])
                st.error(f"⚠️ {len(rows)} product(s) need restocking!")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ All products are well-stocked (≥ 10 units).")
        except Exception as e:
            st.error(f"Error: {e}")

    # ── Customer History ──────────────────────────────────────────────────────
    with tab5:
        st.subheader("Customer Purchase History")
        customers = Customer.get_all_customers()
        if customers:
            opts = {f"{r[1]} (ID {r[0]})": r[0] for r in customers}
            sel  = st.selectbox("Select Customer", list(opts.keys()))
            cid  = opts[sel]

            rows  = Sale.get_sales_by_customer(cid)
            if rows:
                df = pd.DataFrame(rows, columns=["Sale ID", "Date", "Amount ($)"])
                df["Amount ($)"] = df["Amount ($)"].apply(lambda x: f"${float(x):,.2f}")
                st.dataframe(df, use_container_width=True, hide_index=True)
                total = sum(float(r[2]) for r in rows)
                st.metric(f"Total spent by {sel.split(' (')[0]}", f"${total:,.2f}")
            else:
                st.info("No purchase history for this customer.")
        else:
            st.info("No customers found.")


# import streamlit as st
# import pandas as pd
# from datetime import date, timedelta

# from Database import init_db, fetch_one
# from customers import Customer
# from products import Product
# from sales import Sale
# from sales_items import SaleItem


# # --------------------------------------------------
# # PAGE CONFIGURATION
# # --------------------------------------------------

# st.set_page_config(
#     page_title="Smart Inventory Manager",
#     page_icon="📦",
#     layout="wide"
# )


# # --------------------------------------------------
# # DATABASE INITIALIZATION
# # --------------------------------------------------

# @st.cache_resource
# def initialize_database():
#     init_db()
#     return True


# try:
#     initialize_database()
# except Exception as e:
#     st.error(f"Database initialization failed: {e}")
#     st.info(
#         "Check your PostgreSQL credentials and ensure "
#         "the database exists."
#     )
#     st.stop()


# # --------------------------------------------------
# # HELPER FUNCTIONS
# # --------------------------------------------------

# def show_error(error):
#     st.error(f"Something went wrong: {error}")


# def create_dataframe(rows, columns):
#     if rows:
#         return pd.DataFrame(rows, columns=columns)

#     return pd.DataFrame(columns=columns)


# def format_currency(amount):
#     return f"₹{float(amount or 0):,.2f}"


# # --------------------------------------------------
# # SIDEBAR NAVIGATION
# # --------------------------------------------------

# st.sidebar.title("📦 Smart Inventory Manager")
# st.sidebar.caption("Inventory and Sales Management")

# page = st.sidebar.radio(
#     "Navigation",
#     [
#         "Dashboard",
#         "Customers",
#         "Products",
#         "New Sale",
#         "Sales History",
#         "Analytics"
#     ]
# )


# # ==================================================
# # DASHBOARD
# # ==================================================

# if page == "Dashboard":

#     st.title("📊 Inventory Dashboard")
#     st.write("Overview of your inventory and sales.")

#     try:
#         total_products = fetch_one(
#             "SELECT COUNT(*) FROM products"
#         )[0]

#         total_customers = fetch_one(
#             "SELECT COUNT(*) FROM customers"
#         )[0]

#         sales_today = fetch_one(
#             """
#             SELECT COALESCE(SUM(total_amount), 0)
#             FROM sales
#             WHERE sale_date::date = %s
#             """,
#             (date.today(),)
#         )[0]

#         low_stock_count = fetch_one(
#             """
#             SELECT COUNT(*)
#             FROM products
#             WHERE stock_quantity <= reorder_level
#             """
#         )[0]

#         col1, col2, col3, col4 = st.columns(4)

#         col1.metric(
#             "Total Products",
#             total_products
#         )

#         col2.metric(
#             "Total Customers",
#             total_customers
#         )

#         col3.metric(
#             "Today's Sales",
#             format_currency(sales_today)
#         )

#         col4.metric(
#             "Low Stock Products",
#             low_stock_count
#         )

#         # LOW STOCK PRODUCTS
#         st.subheader("⚠️ Low Stock Products")

#         low_stock_products = Product.get_low_stock_products()

#         st.dataframe(
#             create_dataframe(
#                 low_stock_products,
#                 [
#                     "Product ID",
#                     "Product Name",
#                     "Category",
#                     "Price",
#                     "Stock Quantity",
#                     "Reorder Level"
#                 ]
#             ),
#             use_container_width=True,
#             hide_index=True
#         )

#         # RECENT SALES
#         st.subheader("🧾 Recent Sales")

#         recent_sales = Sale.get_all_sales()

#         st.dataframe(
#             create_dataframe(
#                 recent_sales[:10],
#                 [
#                     "Sale ID",
#                     "Sale Date",
#                     "Customer ID",
#                     "Customer Name",
#                     "Total Amount"
#                 ]
#             ),
#             use_container_width=True,
#             hide_index=True
#         )

#         # SALES TREND
#         sales_trend = Sale.get_daily_sales_trend(7)

#         if sales_trend:
#             st.subheader("📈 Sales Trend — Last 7 Days")

#             trend_df = create_dataframe(
#                 sales_trend,
#                 ["Date", "Sales"]
#             )

#             trend_df["Sales"] = pd.to_numeric(
#                 trend_df["Sales"]
#             )

#             st.line_chart(
#                 trend_df.set_index("Date")
#             )

#     except Exception as e:
#         show_error(e)


# # ==================================================
# # CUSTOMERS
# # ==================================================

# elif page == "Customers":

#     st.title("👥 Customer Management")

#     # ADD CUSTOMER
#     with st.expander("➕ Add New Customer"):

#         with st.form("add_customer_form"):

#             name = st.text_input("Customer Name *")
#             email = st.text_input("Email")
#             phone = st.text_input("Phone")
#             address = st.text_area("Address")

#             submitted = st.form_submit_button(
#                 "Add Customer"
#             )

#             if submitted:

#                 if not name.strip():
#                     st.warning(
#                         "Customer name is required."
#                     )

#                 else:
#                     try:
#                         Customer.insert_customer(
#                             name.strip(),
#                             email.strip() or None,
#                             phone.strip() or None,
#                             address.strip() or None
#                         )

#                         st.success(
#                             "Customer added successfully!"
#                         )

#                         st.rerun()

#                     except Exception as e:
#                         show_error(e)

#     # SEARCH CUSTOMERS
#     search = st.text_input(
#         "🔍 Search customer by name, email or phone"
#     )

#     try:
#         if search.strip():
#             customers = Customer.search_customer(
#                 search.strip()
#             )
#         else:
#             customers = Customer.get_all_customers()

#         st.subheader("Customer List")

#         st.dataframe(
#             create_dataframe(
#                 customers,
#                 [
#                     "Customer ID",
#                     "Name",
#                     "Email",
#                     "Phone",
#                     "Address",
#                     "Created At"
#                 ]
#             ),
#             use_container_width=True,
#             hide_index=True
#         )

#     except Exception as e:
#         show_error(e)

#     # UPDATE / DELETE CUSTOMER
#     try:
#         all_customers = Customer.get_all_customers()

#         if all_customers:

#             customer_ids = [
#                 customer[0]
#                 for customer in all_customers
#             ]

#             selected_customer_id = st.selectbox(
#                 "Select customer to manage",
#                 customer_ids,
#                 format_func=lambda customer_id: next(
#                     (
#                         f"{customer[1]} (ID: {customer[0]})"
#                         for customer in all_customers
#                         if customer[0] == customer_id
#                     ),
#                     str(customer_id)
#                 )
#             )

#             customer = Customer.get_customer_by_id(
#                 selected_customer_id
#             )

#             if customer:

#                 with st.expander("✏️ Update Customer"):

#                     with st.form("update_customer_form"):

#                         updated_name = st.text_input(
#                             "Name",
#                             value=customer[1] or ""
#                         )

#                         updated_email = st.text_input(
#                             "Email",
#                             value=customer[2] or ""
#                         )

#                         updated_phone = st.text_input(
#                             "Phone",
#                             value=customer[3] or ""
#                         )

#                         updated_address = st.text_area(
#                             "Address",
#                             value=customer[4] or ""
#                         )

#                         update_button = st.form_submit_button(
#                             "Update Customer"
#                         )

#                         if update_button:

#                             if not updated_name.strip():
#                                 st.warning(
#                                     "Customer name is required."
#                                 )

#                             else:
#                                 try:
#                                     Customer.update_customer(
#                                         selected_customer_id,
#                                         updated_name.strip(),
#                                         updated_email.strip() or None,
#                                         updated_phone.strip() or None,
#                                         updated_address.strip() or None
#                                     )

#                                     st.success(
#                                         "Customer updated successfully!"
#                                     )

#                                     st.rerun()

#                                 except Exception as e:
#                                     show_error(e)

#                 if st.button(
#                     "🗑️ Delete Selected Customer"
#                 ):

#                     try:
#                         Customer.delete_customer(
#                             selected_customer_id
#                         )

#                         st.success(
#                             "Customer deleted successfully."
#                         )

#                         st.rerun()

#                     except Exception as e:
#                         show_error(e)

#     except Exception as e:
#         show_error(e)


# # ==================================================
# # PRODUCTS
# # ==================================================

# elif page == "Products":

#     st.title("📦 Product Management")

#     # ADD PRODUCT
#     with st.expander("➕ Add New Product"):

#         with st.form("add_product_form"):

#             product_name = st.text_input(
#                 "Product Name *"
#             )

#             category = st.text_input(
#                 "Category"
#             )

#             price = st.number_input(
#                 "Price (₹)",
#                 min_value=0.0,
#                 step=1.0
#             )

#             stock_quantity = st.number_input(
#                 "Stock Quantity",
#                 min_value=0,
#                 step=1
#             )

#             reorder_level = st.number_input(
#                 "Reorder Level",
#                 min_value=0,
#                 value=5,
#                 step=1
#             )

#             submitted = st.form_submit_button(
#                 "Add Product"
#             )

#             if submitted:

#                 if not product_name.strip():
#                     st.warning(
#                         "Product name is required."
#                     )

#                 else:
#                     try:
#                         Product.insert_product(
#                             product_name.strip(),
#                             category.strip() or None,
#                             price,
#                             int(stock_quantity),
#                             int(reorder_level)
#                         )

#                         st.success(
#                             "Product added successfully!"
#                         )

#                         st.rerun()

#                     except Exception as e:
#                         show_error(e)

#     # SEARCH PRODUCTS
#     search = st.text_input(
#         "🔍 Search products"
#     )

#     try:
#         if search.strip():
#             products = Product.search_products(
#                 search.strip()
#             )
#         else:
#             products = Product.get_all_products()

#         st.subheader("Product Inventory")

#         st.dataframe(
#             create_dataframe(
#                 products,
#                 [
#                     "Product ID",
#                     "Product Name",
#                     "Category",
#                     "Price",
#                     "Stock Quantity",
#                     "Reorder Level",
#                     "Created At"
#                 ]
#             ),
#             use_container_width=True,
#             hide_index=True
#         )

#     except Exception as e:
#         show_error(e)

#     # UPDATE / DELETE PRODUCT
#     try:
#         all_products = Product.get_all_products()

#         if all_products:

#             product_ids = [
#                 product[0]
#                 for product in all_products
#             ]

#             selected_product_id = st.selectbox(
#                 "Select product to manage",
#                 product_ids,
#                 format_func=lambda product_id: next(
#                     (
#                         f"{product[1]} (ID: {product[0]})"
#                         for product in all_products
#                         if product[0] == product_id
#                     ),
#                     str(product_id)
#                 )
#             )

#             product = Product.get_product_by_id(
#                 selected_product_id
#             )

#             if product:

#                 with st.expander("✏️ Update Product"):

#                     with st.form("update_product_form"):

#                         updated_name = st.text_input(
#                             "Product Name",
#                             value=product[1] or ""
#                         )

#                         updated_category = st.text_input(
#                             "Category",
#                             value=product[2] or ""
#                         )

#                         updated_price = st.number_input(
#                             "Price (₹)",
#                             min_value=0.0,
#                             value=float(product[3]),
#                             step=1.0
#                         )

#                         updated_stock = st.number_input(
#                             "Stock Quantity",
#                             min_value=0,
#                             value=int(product[4]),
#                             step=1
#                         )

#                         updated_reorder = st.number_input(
#                             "Reorder Level",
#                             min_value=0,
#                             value=int(product[5]),
#                             step=1
#                         )

#                         update_button = st.form_submit_button(
#                             "Update Product"
#                         )

#                         if update_button:

#                             if not updated_name.strip():
#                                 st.warning(
#                                     "Product name is required."
#                                 )

#                             else:
#                                 try:
#                                     Product.update_product(
#                                         selected_product_id,
#                                         updated_name.strip(),
#                                         updated_category.strip() or None,
#                                         updated_price,
#                                         int(updated_stock),
#                                         int(updated_reorder)
#                                     )

#                                     st.success(
#                                         "Product updated successfully!"
#                                     )

#                                     st.rerun()

#                                 except Exception as e:
#                                     show_error(e)

#                 if st.button(
#                     "🗑️ Delete Selected Product"
#                 ):

#                     try:
#                         Product.delete_product(
#                             selected_product_id
#                         )

#                         st.success(
#                             "Product deleted successfully."
#                         )

#                         st.rerun()

#                     except Exception as e:
#                         show_error(e)

#     except Exception as e:
#         show_error(e)


# # ==================================================
# # NEW SALE
# # ==================================================

# elif page == "New Sale":

#     st.title("🛒 Create New Sale")

#     try:
#         customers = Customer.get_all_customers()
#         products = Product.get_all_products()

#         if not products:
#             st.info(
#                 "No products found. Add products first."
#             )

#         else:

#             customer_options = [None] + [
#                 customer[0]
#                 for customer in customers
#             ]

#             customer_id = st.selectbox(
#                 "Select Customer (optional)",
#                 customer_options,
#                 format_func=lambda customer_id: (
#                     "Walk-in Customer"
#                     if customer_id is None
#                     else next(
#                         (
#                             f"{customer[1]} (ID: {customer[0]})"
#                             for customer in customers
#                             if customer[0] == customer_id
#                         ),
#                         str(customer_id)
#                     )
#                 )
#             )

#             product_map = {
#                 product[0]: product
#                 for product in products
#             }

#             if "cart" not in st.session_state:
#                 st.session_state.cart = []

#             # ADD PRODUCT TO CART
#             with st.form("add_to_cart_form"):

#                 selected_product_id = st.selectbox(
#                     "Select Product",
#                     list(product_map.keys()),
#                     format_func=lambda product_id: (
#                         f"{product_map[product_id][1]} — "
#                         f"{format_currency(product_map[product_id][3])} "
#                         f"(Stock: {product_map[product_id][4]})"
#                     )
#                 )

#                 quantity = st.number_input(
#                     "Quantity",
#                     min_value=1,
#                     value=1,
#                     step=1
#                 )

#                 add_to_cart = st.form_submit_button(
#                     "Add to Cart"
#                 )

#                 if add_to_cart:

#                     selected_product = product_map[
#                         selected_product_id
#                     ]

#                     already_in_cart = sum(
#                         item["quantity"]
#                         for item in st.session_state.cart
#                         if item["product_id"] == selected_product_id
#                     )

#                     if (
#                         int(quantity) + already_in_cart
#                         > int(selected_product[4])
#                     ):
#                         st.warning(
#                             f"Available stock is "
#                             f"{selected_product[4]} units."
#                         )

#                     else:
#                         st.session_state.cart.append(
#                             {
#                                 "product_id": selected_product_id,
#                                 "quantity": int(quantity)
#                             }
#                         )

#                         st.success(
#                             "Product added to cart."
#                         )

#                         st.rerun()

#             # CART SUMMARY
#             if st.session_state.cart:

#                 st.subheader("🛍️ Shopping Cart")

#                 cart_rows = []
#                 total_amount = 0

#                 for item in st.session_state.cart:

#                     product = product_map[
#                         item["product_id"]
#                     ]

#                     unit_price = float(product[3])

#                     subtotal = (
#                         unit_price * item["quantity"]
#                     )

#                     total_amount += subtotal

#                     cart_rows.append(
#                         (
#                             product[1],
#                             item["quantity"],
#                             unit_price,
#                             subtotal
#                         )
#                     )

#                 st.dataframe(
#                     create_dataframe(
#                         cart_rows,
#                         [
#                             "Product",
#                             "Quantity",
#                             "Unit Price",
#                             "Subtotal"
#                         ]
#                     ),
#                     use_container_width=True,
#                     hide_index=True
#                 )

#                 st.metric(
#                     "Total Amount",
#                     format_currency(total_amount)
#                 )

#                 col1, col2 = st.columns(2)

#                 with col1:

#                     if st.button(
#                         "✅ Complete Sale",
#                         type="primary"
#                     ):

#                         try:
#                             sale_id = Sale.finalize_sale(
#                                 customer_id,
#                                 st.session_state.cart
#                             )

#                             st.session_state.cart = []

#                             st.success(
#                                 f"Sale #{sale_id} completed successfully!"
#                             )

#                             st.rerun()

#                         except Exception as e:
#                             show_error(e)

#                 with col2:

#                     if st.button("🗑️ Clear Cart"):

#                         st.session_state.cart = []

#                         st.rerun()

#     except Exception as e:
#         show_error(e)


# # ==================================================
# # SALES HISTORY
# # ==================================================

# elif page == "Sales History":

#     st.title("🧾 Sales History")

#     try:
#         sales = Sale.get_all_sales()

#         st.dataframe(
#             create_dataframe(
#                 sales,
#                 [
#                     "Sale ID",
#                     "Sale Date",
#                     "Customer ID",
#                     "Customer Name",
#                     "Total Amount"
#                 ]
#             ),
#             use_container_width=True,
#             hide_index=True
#         )

#         if sales:

#             selected_sale_id = st.selectbox(
#                 "Select Sale to View Details",
#                 [sale[0] for sale in sales]
#             )

#             selected_sale = Sale.get_sale_by_id(
#                 selected_sale_id
#             )

#             if selected_sale:

#                 st.subheader(
#                     f"Sale #{selected_sale[0]}"
#                 )

#                 col1, col2 = st.columns(2)

#                 col1.write(
#                     f"**Customer:** {selected_sale[3]}"
#                 )

#                 col2.write(
#                     f"**Total:** "
#                     f"{format_currency(selected_sale[4])}"
#                 )

#                 sale_items = SaleItem.get_items_by_sale(
#                     selected_sale_id
#                 )

#                 st.subheader("Sale Items")

#                 st.dataframe(
#                     create_dataframe(
#                         sale_items,
#                         [
#                             "Sale Item ID",
#                             "Sale ID",
#                             "Product ID",
#                             "Product Name",
#                             "Quantity",
#                             "Unit Price",
#                             "Subtotal"
#                         ]
#                     ),
#                     use_container_width=True,
#                     hide_index=True
#                 )

#     except Exception as e:
#         show_error(e)


# # ==================================================
# # ANALYTICS
# # ==================================================

# elif page == "Analytics":

#     st.title("📈 Sales Analytics")

#     today = date.today()

#     col1, col2 = st.columns(2)

#     with col1:
#         start_date = st.date_input(
#             "Start Date",
#             value=today - timedelta(days=30)
#         )

#     with col2:
#         end_date = st.date_input(
#             "End Date",
#             value=today
#         )

#     if start_date > end_date:

#         st.warning(
#             "Start date cannot be after end date."
#         )

#     else:

#         try:
#             sales = Sale.get_sales_in_range(
#                 start_date,
#                 end_date
#             )

#             sales_df = create_dataframe(
#                 sales,
#                 [
#                     "Sale ID",
#                     "Sale Date",
#                     "Customer Name",
#                     "Total Amount"
#                 ]
#             )

#             total_revenue = sum(
#                 float(sale[3] or 0)
#                 for sale in sales
#             )

#             col1, col2 = st.columns(2)

#             col1.metric(
#                 "Total Revenue",
#                 format_currency(total_revenue)
#             )

#             col2.metric(
#                 "Total Transactions",
#                 len(sales)
#             )

#             st.subheader("Sales in Selected Date Range")

#             st.dataframe(
#                 sales_df,
#                 use_container_width=True,
#                 hide_index=True
#             )

#             # DAILY SALES TREND
#             st.subheader("📊 Daily Sales Trend")

#             sales_trend = Sale.get_daily_sales_trend(30)

#             if sales_trend:

#                 trend_df = create_dataframe(
#                     sales_trend,
#                     ["Date", "Revenue"]
#                 )

#                 trend_df["Revenue"] = pd.to_numeric(
#                     trend_df["Revenue"]
#                 )

#                 st.bar_chart(
#                     trend_df.set_index("Date")
#                 )

#             else:
#                 st.info(
#                     "No sales data available for the trend."
#                 )

#             # TOP SELLING PRODUCTS
#             st.subheader("🏆 Top Selling Products")

#             top_products = Sale.get_top_selling_products(10)

#             st.dataframe(
#                 create_dataframe(
#                     top_products,
#                     [
#                         "Product ID",
#                         "Product Name",
#                         "Units Sold",
#                         "Revenue"
#                     ]
#                 ),
#                 use_container_width=True,
#                 hide_index=True
#             )

#             # CUSTOMER SALES SUMMARY
#             st.subheader("👥 Sales by Customer")

#             customer_sales = Sale.get_sales_by_customer()

#             st.dataframe(
#                 create_dataframe(
#                     customer_sales,
#                     [
#                         "Customer Name",
#                         "Number of Sales",
#                         "Revenue"
#                     ]
#                 ),
#                 use_container_width=True,
#                 hide_index=True
#             )

#         except Exception as e:
#             show_error(e)


# # ==================================================
# # FOOTER
# # ==================================================

# st.sidebar.divider()
# st.sidebar.caption("Smart Inventory Manager")
# st.sidebar.caption("Streamlit + PostgreSQL")
