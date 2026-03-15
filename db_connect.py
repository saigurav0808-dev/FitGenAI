import mysql.connector

print("Testing MySQL connection...")

try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="fituser",
        password="Sai@2006",
        database="fitproject",
        port=3306,
        connection_timeout=5
    )

    if db.is_connected():
        print("SUCCESS: Database connected")

except Exception as e:
    print("ERROR:", e)

print("Program finished")