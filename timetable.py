import sqlite3
from datetime import datetime

# --------------------------
# Database Setup
# --------------------------
conn = sqlite3.connect("shuttle_system.db")
cursor = conn.cursor()

# Create shuttle timetable table
cursor.execute('''
CREATE TABLE IF NOT EXISTS shuttle_timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    trip_status TEXT DEFAULT 'Scheduled'
)
''')
conn.commit()

# --------------------------
# Helper Functions
# --------------------------
def validate_time_format(time_str):
    """Validate HH:MM format (24-hour)"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def display_timetable(rows):
    if not rows:
        print("No timetable available.")
        return
    print(f"{'ID':<3} {'Route':<15} {'Departure':<8} {'Arrival':<8} {'Status':<10}")
    for row in rows:
        print(f"{row[0]:<3} {row[1]:<15} {row[2]:<8} {row[3]:<8} {row[4]:<10}")

# --------------------------
# Admin Functions
# --------------------------
def admin_add_or_update_timetable(route, departure_time, arrival_time, trip_status="Scheduled"):
    if not validate_time_format(departure_time) or not validate_time_format(arrival_time):
        print("Error: Invalid time format. Use HH:MM (24-hour).")
        return

    # Check if route exists
    cursor.execute("SELECT * FROM shuttle_timetable WHERE route=?", (route,))
    row = cursor.fetchone()
    if row:
        # Update existing timetable
        cursor.execute("""
        UPDATE shuttle_timetable
        SET departure_time=?, arrival_time=?, trip_status=?
        WHERE route=?
        """, (departure_time, arrival_time, trip_status, route))
        print(f"Timetable updated for route {route}.")
    else:
        # Add new timetable
        cursor.execute("""
        INSERT INTO shuttle_timetable (route, departure_time, arrival_time, trip_status)
        VALUES (?, ?, ?, ?)
        """, (route, departure_time, arrival_time, trip_status))
        print(f"Timetable added for route {route}.")
    conn.commit()

# --------------------------
# Passenger Function
# --------------------------
def passenger_view_timetable(route):
    cursor.execute("SELECT * FROM shuttle_timetable WHERE route=?", (route,))
    rows = cursor.fetchall()
    display_timetable(rows)

# --------------------------
# Driver Function
# --------------------------
def driver_view_assigned_timetable(route, time_format_12hr=False):
    cursor.execute("SELECT * FROM shuttle_timetable WHERE route=?", (route,))
    rows = cursor.fetchall()
    if time_format_12hr:
        for i, row in enumerate(rows):
            dep = datetime.strptime(row[2], "%H:%M").strftime("%I:%M %p")
            arr = datetime.strptime(row[3], "%H:%M").strftime("%I:%M %p")
            rows[i] = (row[0], row[1], dep, arr, row[4])
    display_timetable(rows)

# --------------------------
# Transport Coordinator Function
# --------------------------
def tc_view_timetable(filter_route=None, filter_date=None):
    query = "SELECT * FROM shuttle_timetable"
    params = []
    if filter_route:
        query += " WHERE route=?"
        params.append(filter_route)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    display_timetable(rows)
    # Conflict detection example (simple check: overlapping times)
    for i in range(len(rows)):
        for j in range(i+1, len(rows)):
            dep_i = datetime.strptime(rows[i][2], "%H:%M")
            arr_i = datetime.strptime(rows[i][3], "%H:%M")
            dep_j = datetime.strptime(rows[j][2], "%H:%M")
            arr_j = datetime.strptime(rows[j][3], "%H:%M")
            if dep_i < arr_j and dep_j < arr_i and rows[i][1] == rows[j][1]:
                print(f"Warning: Schedule conflict detected for route {rows[i][1]} between trips {rows[i][0]} and {rows[j][0]}.")

# --------------------------
# Example Usage
# --------------------------
# Admin adds/updates timetable
admin_add_or_update_timetable("Route A", "08:00", "08:45")
admin_add_or_update_timetable("Route B", "09:00", "09:50")

# Passenger views timetable
print("\nPassenger View:")
passenger_view_timetable("Route A")

# Driver views assigned timetable in 12-hour format
print("\nDriver View (12-hour):")
driver_view_assigned_timetable("Route A", time_format_12hr=True)

# Transport Coordinator views all timetables
print("\nTransport Coordinator View:")
tc_view_timetable()
