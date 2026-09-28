
# 📊 Sales Analytics Dashboard

### Turn sales records into clear business insights.

A lightweight sales management and analytics web application built for
small businesses using **Python Flask, MySQL, and Chart.js**.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualizations-FF6384?logo=chartdotjs&logoColor=white)
![Status](https://img.shields.io/badge/Status-Working-brightgreen)
:::

------------------------------------------------------------------------

## ✨ Overview

The **Sales Analytics Dashboard** helps small businesses manage sales
records and understand business performance through a simple web
interface. Users can add sales manually or import records from a CSV
file, then explore key metrics and visualizations from the dashboard.

The goal is to make everyday sales analysis more accessible without
requiring a complex or expensive business application.

## 🚀 Features

-   📈 **Sales overview** --- view key sales metrics on a dashboard.
-   💰 **Revenue analysis** --- calculate revenue using quantity and
    price.
-   📅 **Monthly trends** --- visualize revenue over time.
-   🗂️ **Category analysis** --- compare revenue across product
    categories.
-   🏆 **Top 5 products** --- identify products with the highest total
    revenue.
-   ➕ **Add sales records** --- enter sales through a web form.
-   🔎 **Browse and filter** --- view, search, and filter sales records.
-   🗑️ **Delete records** --- remove sales entries when needed.
-   📤 **CSV import** --- upload sales data in the supported format.

## 🧰 Tech Stack

  Technology   Purpose
  ------------ --------------------------------
  Python       Backend programming
  Flask        Web application and routing
  MySQL        Store sales records
  SQL          Query and aggregate sales data
  HTML & CSS   Page structure and styling
  JavaScript   Frontend interactions
  Chart.js     Dashboard charts
  Jinja2       Render dynamic HTML templates

## 🖥️ How It Works

``` text
User
  |
  v
Flask Web Application
  |
  +-- Add / Search / Filter / Delete Sales
  +-- Import CSV File
  |
  v
MySQL Database
  |
  v
SQL Aggregations
  +-- Total Revenue
  +-- Sales Record Count
  +-- Average Revenue per Record
  +-- Monthly Revenue
  +-- Revenue by Category
  +-- Top 5 Products
  |
  v
Dashboard Cards & Charts
```

## 📂 Project Structure

``` text
sales-analytics/
├── app.py                  # Flask routes and application logic
├── database.py             # MySQL connection and database operations
├── requirements.txt        # Python dependencies
├── .env.example            # Example configuration (no real secrets)
├── .gitignore              # Files excluded from Git
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── sales.html
│   ├── add_sale.html
│   └── upload.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── dashboard.js
```

## ⚙️ Getting Started

### 1. Prerequisites

Install the following:

-   Python 3.12 or a compatible Python version
-   MySQL Server
-   Git

### 2. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/sales-analytics-dashboard.git
cd sales-analytics-dashboard
```

Replace `YOUR-USERNAME` with your GitHub username.

### 3. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

``` bash
pip install -r requirements.txt
```

### 5. Create the database

Open MySQL Workbench or your MySQL client and run:

``` sql
CREATE DATABASE sales_analytics;
USE sales_analytics;

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    customer_name VARCHAR(255),
    sale_date DATE NOT NULL
);
```

If your project already has this database and table, you do not need to
create them again.

### 6. Configure database connection

Set the environment variables in the terminal where you will run the
application. Replace the example values with your own local MySQL
settings.

**Windows PowerShell:**

``` powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_DATABASE="sales_analytics"
$env:MYSQL_PASSWORD="YOUR_MYSQL_PASSWORD"
```

Keep your real password private. Never commit passwords or a real `.env`
file to GitHub.

### 7. Run the application

``` bash
python app.py
```

Open your browser and visit:

**http://127.0.0.1:5000**

## 📊 Analytics Included

  Metric                       What it tells you
  ---------------------------- ------------------------------------------
  Total revenue                Revenue calculated from quantity × price
  Total sales records          Number of records in the sales table
  Average revenue per record   Average of quantity × price per record
  Monthly revenue              Revenue grouped by month
  Revenue by category          Revenue grouped by product category
  Top 5 products               Products ranked by total revenue

## 🧠 What I Practiced

-   Building a web application with Flask
-   Connecting Python to a MySQL database
-   Writing SQL queries with `SUM()`, `COUNT()`, `AVG()`, `GROUP BY`,
    `ORDER BY`, and `LIMIT`
-   Implementing create, read, and delete operations
-   Validating form input and handling CSV imports
-   Presenting aggregated data through charts and dashboard metrics

## 🔐 Notes

-   CSV files must use the column names expected by the application:
    `product`, `category`, `quantity`, `price`, `customer_name`, and
    `sale_date`.
-   Configure database credentials locally using environment variables.
-   Do not upload private customer information, database exports,
    passwords, or secret keys.
-   This project focuses on descriptive analytics; it does not predict
    future sales.

## 🔮 Possible Future Improvements

-   User authentication and role-based access
-   Date-range filters and exportable reports
-   Pagination for large sales tables
-   Automated tests and improved error logging
-   Deployment to a cloud hosting platform

## 👨‍💻 Author

**Aditya Salunke**

BE --- Artificial Intelligence & Data Science

[GitHub](https://github.com/Adi-08)

------------------------------------------------------------------------


**Built to make sales data easier to manage and understand.** 🚀

If you find this project useful, consider giving the repository a ⭐

