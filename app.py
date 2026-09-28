import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Flask, flash, redirect, render_template, request, url_for

import database

app = Flask(__name__)
app.secret_key = "sales-analytics-local-key"


def validate_sale_values(form):
    product = form.get("product", "").strip()
    category = form.get("category", "").strip()
    customer_name = form.get("customer_name", "").strip()
    quantity_text = form.get("quantity", "").strip()
    price_text = form.get("price", "").strip()
    sale_date = form.get("sale_date", "").strip()
    errors = []

    if not product:
        errors.append("Product is required.")
    if not category:
        errors.append("Category is required.")
    if not customer_name:
        errors.append("Customer name is required.")

    try:
        quantity = int(quantity_text)
        if quantity <= 0:
            errors.append("Quantity must be greater than zero.")
    except ValueError:
        quantity = None
        errors.append("Quantity must be a whole number.")

    try:
        price = Decimal(price_text)
        if price <= 0:
            errors.append("Price must be greater than zero.")
    except (InvalidOperation, ValueError):
        price = None
        errors.append("Price must be a valid number.")

    try:
        datetime.strptime(sale_date, "%Y-%m-%d")
    except ValueError:
        errors.append("Sale date must use YYYY-MM-DD format.")

    return errors, (product, category, quantity, price, customer_name, sale_date)


@app.route("/")
def dashboard():
    try:
        stats = database.get_dashboard_stats()
        monthly_revenue = database.get_monthly_revenue()
        category_revenue = database.get_category_revenue()
        top_products = database.get_top_products()
        recent_sales = database.get_sales()[:5]
    except Exception as error:
        flash(f"Could not load dashboard data: {error}", "error")
        stats = {
            "total_revenue": 0,
            "total_orders": 0,
            "total_quantity": 0,
            "average_order_value": 0,
        }
        monthly_revenue, category_revenue, top_products, recent_sales = [], [], [], []

    return render_template(
        "dashboard.html",
        stats=stats,
        monthly_revenue=monthly_revenue,
        category_revenue=category_revenue,
        top_products=top_products,
        recent_sales=recent_sales,
    )


@app.route("/sales")
def sales():
    search_text = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    try:
        sales_rows = database.get_sales(search_text, category)
        categories = database.get_categories()
    except Exception as error:
        flash(f"Could not load sales: {error}", "error")
        sales_rows, categories = [], []
    return render_template(
        "sales.html",
        sales=sales_rows,
        categories=categories,
        search_text=search_text,
        selected_category=category,
    )


@app.route("/add-sale", methods=["GET", "POST"])
def add_sale():
    if request.method == "POST":
        errors, values = validate_sale_values(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("add_sale.html", form=request.form)

        try:
            database.add_sale(*values)
            flash("Sale added successfully.", "success")
            return redirect(url_for("sales"))
        except Exception as error:
            flash(f"Could not add sale: {error}", "error")
            return render_template("add_sale.html", form=request.form)

    return render_template("add_sale.html", form={})


@app.post("/delete-sale/<int:sale_id>")
def delete_sale(sale_id):
    try:
        database.delete_sale(sale_id)
        flash("Sale deleted successfully.", "success")
    except Exception as error:
        flash(f"Could not delete sale: {error}", "error")
    return redirect(url_for("sales"))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file or not uploaded_file.filename:
            flash("Choose a CSV file to upload.", "error")
            return render_template("upload.html")
        if not uploaded_file.filename.lower().endswith(".csv"):
            flash("Only CSV files are supported.", "error")
            return render_template("upload.html")

        try:
            text = uploaded_file.stream.read().decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))
            required_columns = {
                "product", "category", "quantity", "price", "customer_name", "sale_date"
            }
            columns = set(reader.fieldnames or [])
            missing_columns = required_columns - columns
            if missing_columns:
                flash(
                    "Missing required columns: " + ", ".join(sorted(missing_columns)),
                    "error",
                )
                return render_template("upload.html")

            imported_count = 0
            errors = []
            for row_number, row in enumerate(reader, start=2):
                row_errors, values = validate_sale_values(row)
                if row_errors:
                    errors.append(f"Row {row_number}: {' '.join(row_errors)}")
                    continue
                try:
                    database.add_sale(*values)
                    imported_count += 1
                except Exception as error:
                    errors.append(f"Row {row_number}: database error: {error}")

            if imported_count:
                flash(f"Imported {imported_count} sale(s) successfully.", "success")
            if errors:
                for error in errors[:10]:
                    flash(error, "error")
                if len(errors) > 10:
                    flash(f"There were {len(errors) - 10} more invalid row(s).", "error")
        except UnicodeDecodeError:
            flash("The CSV file must use UTF-8 encoding.", "error")
        except Exception as error:
            flash(f"Could not process the CSV file: {error}", "error")

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
