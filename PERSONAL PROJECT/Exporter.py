import sqlite3
import csv
from datetime import datetime

# Connect to your SQLite database
conn = sqlite3.connect(r'c:\PERSONAL PROJECT\instance\test.db')
cursor = conn.cursor()

# Query all data from the todo_item table
cursor.execute("SELECT id, task, deadline, completed FROM todo_item")
rows = cursor.fetchall()

# Format deadline to only show date
formatted_rows = []
for row in rows:
    id, task, deadline, completed = row
    if deadline:
        # Try parsing with time, fallback to just date
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            deadline_str = deadline_date.strftime("%Y-%m-%d")
        except Exception:
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                deadline_str = deadline_date.strftime("%Y-%m-%d")
            except Exception:
                deadline_str = deadline  # fallback if already formatted
    else:
        deadline_str = ""
    formatted_rows.append([id, task, deadline_str, completed])

# Write to CSV
with open(r'c:\PERSONAL PROJECT\todo_item.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'task', 'deadline', 'completed'])
    writer.writerows(formatted_rows)

# Export user table as before
cursor.execute("SELECT id, username, grad_year, purpose FROM user")
user_rows = cursor.fetchall()
with open(r'c:\PERSONAL PROJECT\user.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'username', 'grad_year', 'purpose'])
    writer.writerows(user_rows)

conn.close()
print("Exported todo_item and user tables to CSV files")