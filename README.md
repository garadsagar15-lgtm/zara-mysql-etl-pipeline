# Zara MySQL ETL Pipeline with Python

A beginner-friendly ETL workflow that uses Python and MySQL to load Zara product data from a CSV file, clean and convert its values, and create separate tables for exploring product prices and sales volume.

## Overview

The pipeline uses `mysql-connector-python` to connect to MySQL, creates the `ETl` database and a `Zara_Sales` table, then loads product records from the semicolon-delimited `zara.csv` file. It demonstrates common SQL operations by creating 12 derived tables for analysis.

## ETL workflow

1. **Extract** product rows from `zara.csv` using Python's `csv.DictReader`.
2. **Transform** the values by converting product IDs, sales volume, prices, and scrape timestamps, and storing empty cells as `NULL`.
3. **Load** the records into MySQL with a batch insert. Existing `Product_ID` rows are updated on rerun.
4. **Analyze** the loaded data with SQL filters, sorting, grouping, aggregates, and a `CASE` statement.

## Tables created

| Table | Example operation |
|---|---|
| `Zara_Backup_All` | Copy all Zara product rows |
| `Zara_Backup_High_Sales` | Filter products with sales volume above 2,000 |
| `Zara_Backup_Selected_Columns` | Keep product ID, name, price, and sales volume |
| `Zara_Backup_Terms` | Select distinct product search terms |
| `Zara_Backup_Sales_Sorted` | Sort products by sales volume descending |
| `Zara_Backup_Product_Count` | Count products by search term |
| `Zara_Backup_Average_Price` | Calculate average price and sales volume by term |
| `Zara_Backup_High_Average_Sales` | Keep terms with average sales volume above 1,800 |
| `Zara_Backup_Price_Range` | Filter prices between 30 and 100 |
| `Zara_Backup_Selected_Types` | Select products with terms `jackets` or `shoes` |
| `Zara_Backup_Name_Search` | Find product names containing `JACKET` |
| `Zara_Backup_Sales_Category` | Categorize sales as High, Medium, or Low with `CASE` |

> The filters and thresholds are examples and can be adjusted in the SQL queries to explore the dataset in different ways.

## Screenshots

### ETL workflow

<img src="zara_mysql_etl_workflow.svg" alt="Workflow showing Zara CSV extraction, Python cleaning, MySQL loading, and SQL analysis" width="100%">

The image file is [`zara_mysql_etl_workflow.svg`](zara_mysql_etl_workflow.svg). GitHub renders it directly from the repository.

### MySQL Workbench results

To show your run results, add a screenshot of the `ETl` schema and created tables to `assets/mysql-workbench.png`, then include it like this:

```html
<img src="assets/mysql-workbench.png" alt="MySQL Workbench showing the Zara ETL tables" width="100%">
```

## Requirements

- Python 3
- MySQL Server
- MySQL Workbench (optional, for browsing tables and query results)
- Python package: `mysql-connector-python`

Install the connector:

```bash
python -m pip install mysql-connector-python
```

## Configure the database connection

Update `CSV_FILE` in the Python script if your `zara.csv` file is stored in a different location. The supplied CSV uses a semicolon (`;`) delimiter.

Set the MySQL host, username, and password to match your local MySQL installation. Do not publish your password in the Python file or commit it to GitHub. You can read connection details from environment variables instead:

```python
import os
import mysql.connector

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE", "ETl"),
)
```

The MySQL account needs permission to create the database and tables. In this project, the script creates the `ETl` database if it does not already exist.

## Run

1. Start MySQL Server.
2. Install `mysql-connector-python`.
3. Set your local MySQL connection details in the script or environment variables.
4. Make sure `CSV_FILE` points to `zara.csv`.
5. Run the Python script from the VS Code terminal:

   ```bash
   python etl_pipeline.py
   ```

If you save the script with a different filename, replace `etl_pipeline.py` with that filename. After it completes, refresh the schema in MySQL Workbench and inspect `Zara_Sales` and the 12 `Zara_Backup_*` tables.

## Notes

- The script drops and recreates each `Zara_Backup_*` table every time it runs, so each analysis table reflects the latest `Zara_Sales` data.
- `Zara_Sales` uses `Product_ID` as its primary key. Re-running the import updates existing products with matching IDs.
- The dataset contains a product sales-volume field; it does not include transaction-level sales history or revenue.
- Review the dataset's license or source terms before committing `zara.csv` to a public repository.

## License

Add a license file if you intend to share or reuse this project publicly.
