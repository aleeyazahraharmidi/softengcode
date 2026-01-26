import sqlite3
from datetime import datetime

# ---------------------------
# Database setup (SQLite for demo)
# ---------------------------
conn = sqlite3.connect('shuttle_system.db')
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS routes (
    route_id INTEGER PRIMARY KEY,
    route_name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT CHECK(role IN ('Driver','Transport Coordinator','Admin'))
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS route_assignments (
    assignment_id INTEGER PRIMARY KEY,
    route_id INTEGER,
    driver_id INTEGER,
    coordinator_id INTEGER,
    trip_date TEXT,
    FOREIGN KEY(route_id) REFERENCES routes(route_id),
    FOREIGN KEY(driver_id) REFERENCES users(user_id),
    FOREIGN KEY(coordinator_id) REFERENCES users(user_id)
)
''')

conn.commit()

# ---------------------------
# Core Functions
# ---------------------------

def check_conflict(driver_id, trip_date):
    """
    Check if driver already has an assignment on the same date.
    """
    cursor.execute('''
        SELECT * FROM route_assignments
        WHERE driver_id = ? AND trip_date = ?
    ''', (driver_id, trip_date))
    return cursor.fetchone() is not None

def assign_route(route_id, driver_id, coordinator_id, trip_date):
    """
    Assigns driver and coordinator to a route, checking for conflicts.
    """
    # Conflict check
    if check_conflict(driver_id, trip_date):
        print(f"Error: Driver {driver_id} already assigned on {trip_date}")
        return False

    # Save assignment
    cursor.execute('''
        INSERT INTO route_assignments (route_id, driver_id, coordinator_id, trip_date)
        VALUES (?, ?, ?, ?)
    ''', (route_id, driver_id, coordinator_id, trip_date))
    conn.commit()
    print(f"Assignment successful: Route {route_id} -> Driver {driver_id}, Coordinator {coordinator_id} on {trip_date}")
    return True

# ---------------------------
# Demo Usage
# ---------------------------

# Example data
cursor.execute("INSERT OR IGNORE INTO routes (route_id, route_name) VALUES (1, 'Route A')")
cursor.execute("INSERT OR IGNORE INTO users (user_id, name, role) VALUES (101, 'Alice', 'Driver')")
cursor.execute("INSERT OR IGNORE INTO users (user_id, name, role) VALUES (201, 'Bob', 'Transport Coordinator')")
conn.commit()

# Admin assigns a driver and coordinator to Route A for a specific date
trip_date = '2026-01-26'
assign_route(route_id=1, driver_id=101, coordinator_id=201, trip_date=trip_date)

# Trying to assign the same driver to another route on the same date
assign_route(route_id=1, driver_id=101, coordinator_id=201, trip_date=trip_date)

# ---------------------------
# Close DB connection
# ---------------------------
conn.close()
