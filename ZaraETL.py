import csv
from datetime import datetime
import mysql.connector

CSV_FILE = r"C:\Users\SAGAR\Downloads\zara.csv"

# NOTE: zara.csv uses ';' (semicolon) as the delimiter, not ','
DELIMITER = ";"

# 1. Connect to MySQL server and create the database if needed
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)
cursor = con.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS ETl")
cursor.close()
con.close()

# 2. Connect to the etl database
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ETl"
)
cursor = con.cursor()

print("Connected to MySQL")

# =========================================================
# CREATE THE ZARA SALES TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS Zara_Sales (
    Product_ID INT NOT NULL,
    Product_Position VARCHAR(20),
    Promotion VARCHAR(3),
    Product_Category VARCHAR(30),
    Seasonal VARCHAR(3),
    Sales_Volume INT,
    Brand VARCHAR(20),
    Url VARCHAR(255),
    Sku VARCHAR(30),
    Name VARCHAR(100),
    Description TEXT,
    Price DECIMAL(10, 2),
    Currency VARCHAR(5),
    Scraped_At DATETIME(6),
    Terms VARCHAR(30),
    Section VARCHAR(10),
    PRIMARY KEY (Product_ID)
)
""")

# =========================================================
# LOAD CSV DATA INTO MYSQL
# =========================================================

def clean(value):
    """Return None for empty cells so MySQL stores NULL instead of ''."""
    value = value.strip()
    return value if value != "" else None


with open(CSV_FILE, mode="r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, delimiter=DELIMITER)

    rows = []
    for row in reader:
        rows.append((
            int(row["Product ID"]),
            clean(row["Product Position"]),
            clean(row["Promotion"]),
            clean(row["Product Category"]),
            clean(row["Seasonal"]),
            int(row["Sales Volume"]),
            clean(row["brand"]),
            clean(row["url"]),
            clean(row["sku"]),
            clean(row["name"]),
            clean(row["description"]),
            float(row["price"]),
            clean(row["currency"]),
            datetime.strptime(row["scraped_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            clean(row["terms"]),
            clean(row["section"])
        ))

cursor.executemany("""
    INSERT INTO Zara_Sales
    (Product_ID, Product_Position, Promotion, Product_Category, Seasonal,
     Sales_Volume, Brand, Url, Sku, Name, Description, Price, Currency,
     Scraped_At, Terms, Section)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        Product_Position = VALUES(Product_Position),
        Promotion = VALUES(Promotion),
        Product_Category = VALUES(Product_Category),
        Seasonal = VALUES(Seasonal),
        Sales_Volume = VALUES(Sales_Volume),
        Brand = VALUES(Brand),
        Url = VALUES(Url),
        Sku = VALUES(Sku),
        Name = VALUES(Name),
        Description = VALUES(Description),
        Price = VALUES(Price),
        Currency = VALUES(Currency),
        Scraped_At = VALUES(Scraped_At),
        Terms = VALUES(Terms),
        Section = VALUES(Section)
""", rows)

con.commit()
print(f"Zara sales data loaded successfully ({len(rows)} rows)")


# =========================================================
# 1. SELECT ALL DATA
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_All")
cursor.execute("""
CREATE TABLE Zara_Backup_All AS
SELECT *
FROM Zara_Sales
""")

print("1. All data extracted")


# =========================================================
# 2. WHERE - FILTER DATA
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_High_Sales")
cursor.execute("""
CREATE TABLE Zara_Backup_High_Sales AS
SELECT *
FROM Zara_Sales
WHERE Sales_Volume > 2000
""")

print("2. Filtered data extracted")


# =========================================================
# 3. SELECT SPECIFIC COLUMNS
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Selected_Columns")
cursor.execute("""
CREATE TABLE Zara_Backup_Selected_Columns AS
SELECT Product_ID, Name, Price, Sales_Volume
FROM Zara_Sales
""")

print("3. Selected columns extracted")


# =========================================================
# 4. DISTINCT
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Terms")
cursor.execute("""
CREATE TABLE Zara_Backup_Terms AS
SELECT DISTINCT Terms
FROM Zara_Sales
""")

print("4. Distinct product types extracted")


# =========================================================
# 5. ORDER BY
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Sales_Sorted")
cursor.execute("""
CREATE TABLE Zara_Backup_Sales_Sorted AS
SELECT *
FROM Zara_Sales
ORDER BY Sales_Volume DESC
""")

print("5. Sorted data extracted")


# =========================================================
# 6. GROUP BY + COUNT
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Product_Count")
cursor.execute("""
CREATE TABLE Zara_Backup_Product_Count AS
SELECT Terms, COUNT(*) AS Product_Count
FROM Zara_Sales
GROUP BY Terms
""")

print("6. Product count extracted")


# =========================================================
# 7. GROUP BY + AVG
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Average_Price")
cursor.execute("""
CREATE TABLE Zara_Backup_Average_Price AS
SELECT Terms, AVG(Price) AS Average_Price, AVG(Sales_Volume) AS Average_Sales_Volume
FROM Zara_Sales
GROUP BY Terms
""")

print("7. Average price and sales extracted")


# =========================================================
# 8. HAVING
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_High_Average_Sales")
cursor.execute("""
CREATE TABLE Zara_Backup_High_Average_Sales AS
SELECT Terms, AVG(Sales_Volume) AS Average_Sales_Volume
FROM Zara_Sales
GROUP BY Terms
HAVING AVG(Sales_Volume) > 1800
""")

print("8. HAVING result extracted")


# =========================================================
# 9. BETWEEN
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Price_Range")
cursor.execute("""
CREATE TABLE Zara_Backup_Price_Range AS
SELECT *
FROM Zara_Sales
WHERE Price BETWEEN 30 AND 100
""")

print("9. BETWEEN result extracted")


# =========================================================
# 10. IN
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Selected_Types")
cursor.execute("""
CREATE TABLE Zara_Backup_Selected_Types AS
SELECT *
FROM Zara_Sales
WHERE Terms IN ('jackets', 'shoes')
""")

print("10. IN result extracted")


# =========================================================
# 11. LIKE
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Name_Search")
cursor.execute("""
CREATE TABLE Zara_Backup_Name_Search AS
SELECT *
FROM Zara_Sales
WHERE Name LIKE '%JACKET%'
""")

print("11. LIKE result extracted")


# =========================================================
# 12. CASE
# =========================================================

cursor.execute("DROP TABLE IF EXISTS Zara_Backup_Sales_Category")
cursor.execute("""
CREATE TABLE Zara_Backup_Sales_Category AS
SELECT
    Product_ID,
    Name,
    Sales_Volume,
    CASE
        WHEN Sales_Volume >= 2500 THEN 'High'
        WHEN Sales_Volume >= 1500 THEN 'Medium'
        ELSE 'Low'
    END AS Sales_Category
FROM Zara_Sales
""")

print("12. CASE result extracted")


# =========================================================
# SAVE ALL CHANGES
# =========================================================

con.commit()

print("\nETL completed successfully!")


# =========================================================
# SHOW CREATED TABLES
# =========================================================

cursor.execute("SHOW TABLES")

print("\nTables in database:")

for table in cursor.fetchall():
    print(table[0])


# =========================================================
# CLOSE CONNECTION
# =========================================================

cursor.close()
con.close()

print("\nMySQL connection closed")
