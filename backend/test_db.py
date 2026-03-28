import pyodbc

# Try different connection strings one by one
connections = [
    # Try 1: With instance name
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-JPSKD334\\SQLEXPRESS;DATABASE=farmsense;Trusted_Connection=yes;TrustServerCertificate=yes;',
    
    # Try 2: With localhost
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=farmsense;Trusted_Connection=yes;TrustServerCertificate=yes;',
    
    # Try 3: With dot notation
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=.\\SQLEXPRESS;DATABASE=farmsense;Trusted_Connection=yes;TrustServerCertificate=yes;',

    # Try 4: With port
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,1433;DATABASE=farmsense;Trusted_Connection=yes;TrustServerCertificate=yes;',

    # Try 5: Old SQL Server driver
    'DRIVER={SQL Server};SERVER=LAPTOP-JPSKD334\\SQLEXPRESS;DATABASE=farmsense;Trusted_Connection=yes;',
]

for i, conn_str in enumerate(connections, 1):
    try:
        conn = pyodbc.connect(conn_str, timeout=3)
        print(f"✅ Try {i} WORKED: {conn_str[:60]}")
        conn.close()
        break
    except Exception as e:
        print(f"❌ Try {i} Failed: {str(e)[:80]}")