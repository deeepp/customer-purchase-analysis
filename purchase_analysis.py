import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite database
conn = sqlite3.connect("customer_purchases.db")
cursor = conn.cursor()

# Drop the table if it exists (useful for debugging)
cursor.execute("DROP TABLE IF EXISTS purchases;")

# Create the 'purchases' table with more detailed schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        product_name TEXT,
        purchase_date TEXT,
        quantity INTEGER,
        price REAL
    );
""")

# Extended sample data for insertion
sample_data = [
    (101, "Laptop", "2024-01-10", 2, 800.00),
    (102, "Phone", "2024-02-15", 3, 500.00),
    (103, "Laptop", "2024-03-20", 1, 800.00),
    (101, "Headphones", "2024-01-22", 5, 50.00),
    (104, "Tablet", "2024-04-05", 2, 300.00),
    (102, "Phone", "2024-03-28", 1, 500.00),
    (105, "Smartwatch", "2024-02-25", 4, 150.00),
    (106, "Laptop", "2024-04-10", 3, 800.00),
    (107, "Tablet", "2024-01-30", 1, 300.00),
    (108, "Phone", "2024-03-12", 2, 500.00),
    (109, "Headphones", "2024-04-01", 6, 50.00),
    (110, "Smartwatch", "2024-02-18", 2, 150.00),
    (111, "Headphones", "2024-03-25", 3, 50.00),
    (112, "Phone", "2024-04-20", 1, 500.00),
    (113, "Laptop", "2024-01-18", 1, 800.00),
    (114, "Smartwatch", "2024-02-05", 5, 150.00),
    (115, "Tablet", "2024-03-03", 3, 300.00),
    (116, "Laptop", "2024-04-15", 2, 800.00),
]

# Insert extended sample data into the table
cursor.executemany("INSERT INTO purchases (customer_id, product_name, purchase_date, quantity, price) VALUES (?, ?, ?, ?, ?);", sample_data)
conn.commit()

# 1. Calculate Total Purchases Per Customer
query1 = """
SELECT customer_id, SUM(quantity * price) AS TotalSpent
FROM purchases
GROUP BY customer_id
ORDER BY TotalSpent DESC;
"""
df1 = pd.read_sql_query(query1, conn)

# Export results to Excel
df1.to_excel('total_purchases_per_customer.xlsx', index=False)

# Plotting the total purchases per customer
plt.figure(figsize=(10, 6))
sns.barplot(x='customer_id', y='TotalSpent', data=df1, palette='viridis')
plt.title('Total Purchases Per Customer')
plt.xlabel('Customer ID')
plt.ylabel('Total Spent ($)')
plt.tight_layout()
plt.savefig('total_purchases_per_customer.png')

# 2. Find the Most Popular Product
query2 = """
SELECT product_name, SUM(quantity) AS TotalSold
FROM purchases
GROUP BY product_name
ORDER BY TotalSold DESC
LIMIT 1;
"""
df2 = pd.read_sql_query(query2, conn)

# Plotting the most popular product
plt.figure(figsize=(8, 5))
sns.barplot(x='TotalSold', y='product_name', data=df2, palette='Blues_d')
plt.title('Most Popular Product')
plt.xlabel('Total Units Sold')
plt.ylabel('Product Name')
plt.tight_layout()
plt.savefig('most_popular_product.png')

# 3. Analyze Sales Trends Over Time (Monthly)
query3 = """
SELECT strftime('%Y-%m', purchase_date) AS Month, SUM(quantity * price) AS MonthlyRevenue
FROM purchases
GROUP BY Month
ORDER BY Month;
"""
df3 = pd.read_sql_query(query3, conn)

# Export monthly revenue data to Excel for further analysis
df3.to_excel('monthly_sales_trends.xlsx', index=False)

# Plotting sales trends over time (line graph)
plt.figure(figsize=(10, 6))
sns.lineplot(x='Month', y='MonthlyRevenue', data=df3, marker='o', color='green')
plt.title('Sales Trends Over Time (Monthly)')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('sales_trends_over_time.png')

# Closing the connection to the database
conn.close()

# Inform user about the exported data
print("Query results exported to Excel and visualizations saved as PNG images.")
