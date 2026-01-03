import sqlite3

def check_json_extract():
    conn = sqlite3.connect('backend/lecla.db')
    cursor = conn.cursor()
    try:
        query = "SELECT json_extract(data, '$.date_created') FROM budgets LIMIT 5"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("json_extract worked!")
        print(rows)
    except Exception as e:
        print(f"json_extract failed: {e}")
    conn.close()

if __name__ == "__main__":
    check_json_extract()
