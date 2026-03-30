
import sqlite3
import datetime

conn = sqlite3.connect('jelly.db')
c = conn.cursor()
try:
    c.execute("SELECT timestamp, trigger_type, details, length(raw_snapshot) FROM forensic_events ORDER BY timestamp DESC LIMIT 1")
    row = c.fetchone()
    if row:
        ts = datetime.datetime.fromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Time: {ts}")
        print(f"Trigger: {row[1]}")
        print(f"Details: {row[2]}")
        print(f"Snapshot Size: {row[3]} chars")
    else:
        print("No events found")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
