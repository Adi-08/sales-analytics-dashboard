import os

import mysql.connector


def get_connection():
    """Create a connection using environment variables set on the local machine."""
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")

    if not user or password is None:
        raise RuntimeError(
            "Set MYSQL_USER and MYSQL_PASSWORD environment variables before running the app."
        )

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=user,
        password=password,
        database=os.getenv("MYSQL_DATABASE", "sales_analytics"),
    )


def add_sale(product, category, quantity, price, customer_name, sale_date):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO sales
                (product, category, quantity, price, customer_name, sale_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (product, category, quantity, price, customer_name, sale_date),
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def get_sales(search_text="", category=""):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT id, product, category, quantity, price,
                   quantity * price AS revenue,
                   customer_name, sale_date
            FROM sales
            WHERE (product LIKE %s OR customer_name LIKE %s)
              AND category LIKE %s
            ORDER BY sale_date DESC, id DESC
        """
        search_pattern = f"%{search_text}%"
        category_pattern = f"%{category}%"
        cursor.execute(query, (search_pattern, search_pattern, category_pattern))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_categories():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT category FROM sales ORDER BY category")
        return [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()


def delete_sale(sale_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def get_dashboard_stats():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT
                COALESCE(SUM(quantity * price), 0) AS total_revenue,
                COUNT(*) AS total_orders,
                COALESCE(SUM(quantity), 0) AS total_quantity,
                COALESCE(AVG(quantity * price), 0) AS average_order_value
            FROM sales
        """
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def get_monthly_revenue():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month,
                   SUM(quantity * price) AS revenue
            FROM sales
            GROUP BY month
            ORDER BY month
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_category_revenue():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT category, SUM(quantity * price) AS revenue
            FROM sales
            GROUP BY category
            ORDER BY revenue DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_top_products():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT product, SUM(quantity * price) AS revenue
            FROM sales
            GROUP BY product
            ORDER BY revenue DESC
            LIMIT 5
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
