import sqlite3

def main():
    conn = sqlite3.connect('mock_server(cloud)/cloud_db.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT * FROM dynamic_api_v1_devices WHERE serial_number='gl-db-011'")
    row = cur.fetchone()
    print("Row for gl-db-011:", row)
    
    cur.execute("SELECT COUNT(*) FROM dynamic_api_v1_devices")
    count = cur.fetchone()[0]
    print("Total devices in SQLite dynamic_api_v1_devices:", count)

if __name__ == "__main__":
    main()
