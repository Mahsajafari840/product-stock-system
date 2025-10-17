import streamlit as st
import mysql.connector
from mysql.connector import Error
from decimal import Decimal

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '1234'
DB_NAME = 'final-project'

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def create_product(product_name, product_id, stock, price, description):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO product (product_name, product_id, stock, price, description) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (product_name, product_id, stock, price, description))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Product added successfully!")

def update_product(product_id, product_name, stock, price, description):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        UPDATE product
        SET product_name=%s, stock=%s, price=%s, description=%s
        WHERE product_id=%s
        """
        cursor.execute(query, (product_name, stock, price, description, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Product updated successfully!")

def delete_product(product_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM product WHERE product_id=%s"
        cursor.execute(query, (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Product deleted successfully!")

def list_products():
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    return []

def search_product(product_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM product WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        return product
    return None

def main():
    st.title("Product Management")

    menu = ["Add Product", "Update Product", "Delete Product", "List Products", "Search Product"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Product":
        st.subheader("Add New Product")
        product_name = st.text_input("Product Name")
        product_id = st.text_input("Product ID")
        stock = st.number_input("Number in Stock", min_value=0, step=1)
        price = st.number_input("Price", min_value=0, step=1, format="%d")
        description = st.text_area("Description")

        if st.button("Add Product"):
            if product_name and product_id:
                create_product(product_name, product_id, int(stock), int(price), description)
            else:
                st.error("Please provide both Product Name and Product ID")

    elif choice == "Update Product":
        st.subheader("Update Product")
        product_id = st.text_input("Enter Product ID to Update")
        if product_id:
            products = list_products()
            product = next((p for p in products if p['product_id'] == product_id), None)
            if product:
                stock_val = int(product['stock']) if product['stock'] is not None else 0
                
                if isinstance(product['price'], Decimal):
                    price_val = int(product['price'])
                else:
                    try:
                        price_val = int(float(product['price']))
                    except (TypeError, ValueError):
                        price_val = 0

                product_name = st.text_input("Product Name", product['product_name'])
                stock = st.number_input("Number in Stock", min_value=0, step=1, value=stock_val)
                price = st.number_input("Price", min_value=0, step=1, format="%d", value=price_val)
                description = st.text_area("Description", product['description'])

                if st.button("Update Product"):
                    update_product(product_id, product_name, int(stock), int(price), description)
            else:
                st.warning("Product ID not found.")

    elif choice == "Delete Product":
        st.subheader("Delete Product")
        product_id = st.text_input("Enter Product ID to Delete")

        if st.button("Delete Product"):
            if product_id:
                delete_product(product_id)
            else:
                st.error("Please enter a Product ID")

    elif choice == "List Products":
        st.subheader("Product List")
        products = list_products()
        if products:
            st.table(products)
        else:
            st.info("No products found.")

    elif choice == "Search Product":
        st.subheader("Search Product by Product ID")
        search_id = st.text_input("Enter Product ID to Search")
        if st.button("Search"):
            if search_id:
                product = search_product(search_id)
                if product:
                    st.write("### Product Details:")
                    st.write(f"**Product ID:** {product['product_id']}")
                    st.write(f"**Product Name:** {product['product_name']}")
                    st.write(f"**Stock:** {product['stock']}")
                    st.write(f"**Price:** {int(product['price']) if product['price'] is not None else 0}")
                    st.write(f"**Description:** {product['description']}")
                else:
                    st.warning("Product not found.")
            else:
                st.error("Please enter a Product ID to search.")

if __name__ == "__main__":
    main()
