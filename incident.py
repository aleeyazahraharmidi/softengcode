import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('incident_system.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT CHECK(role IN ('Passenger','Driver','TC','Admin')) NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS incidents (
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reporter_id INTEGER,
    type TEXT,
    location TEXT,
    description TEXT,
    status TEXT CHECK(status IN ('New','In Progress','Resolved')) DEFAULT 'New',
    priority TEXT CHECK(priority IN ('Low','Medium','High')) DEFAULT 'Low',
    assigned_resource TEXT,
    timestamp TEXT,
    FOREIGN KEY (reporter_id) REFERENCES users(user_id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS incident_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    action TEXT,
    timestamp TEXT,
    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
)
''')

conn.commit()


# ----- INCIDENT FUNCTIONS -----

# Submit incident report (Passenger/Driver)
def submit_incident(reporter_id, incident_type, location, description, priority='Low'):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO incidents (reporter_id, type, location, description, priority, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (reporter_id, incident_type, location, description, priority, timestamp))
    incident_id = c.lastrowid
    log_incident(incident_id, f"Incident submitted by user {reporter_id}")
    conn.commit()
    print(f"Incident {incident_id} submitted successfully.")


# View incident status (Passenger/Driver)
def view_incident_status(reporter_id):
    c.execute('''
        SELECT incident_id, type, status, timestamp FROM incidents
        WHERE reporter_id = ?
    ''', (reporter_id,))
    incidents = c.fetchall()
    if not incidents:
        print("No incidents submitted.")
        return
    for inc in incidents:
        print(f"ID: {inc[0]}, Type: {inc[1]}, Status: {inc[2]}, Time: {inc[3]}")


# Monitor incidents (Transport Coordinator)
def monitor_incidents(filter_by=None, filter_value=None):
    query = "SELECT * FROM incidents"
    if filter_by and filter_value:
        query += f" WHERE {filter_by} = ?"
        c.execute(query, (filter_value,))
    else:
        c.execute(query)
    incidents = c.fetchall()
    for inc in incidents:
        print(inc)


# Classify and update incident status (Admin)
def update_incident_status(incident_id, new_status, assigned_resource=None):
    c.execute('SELECT * FROM incidents WHERE incident_id = ?', (incident_id,))
    if not c.fetchone():
        print("Error: Incident not found.")
        return
    c.execute('''
        UPDATE incidents
        SET status = ?, assigned_resource = ?
        WHERE incident_id = ?
    ''', (new_status, assigned_resource, incident_id))
    log_incident(incident_id, f"Status updated to {new_status}")
    conn.commit()
    print(f"Incident {incident_id} updated to {new_status}.")


# View incident reports (Transport Coordinator/Admin)
def view_incident_reports(filter_by=None, filter_value=None):
    query = "SELECT * FROM incidents"
    if filter_by and filter_value:
        query += f" WHERE {filter_by} = ?"
        c.execute(query, (filter_value,))
    else:
        c.execute(query)
    incidents = c.fetchall()
    for inc in incidents:
        print(inc)


# Logging activity
def log_incident(incident_id, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO incident_logs (incident_id, action, timestamp)
        VALUES (?, ?, ?)
    ''', (incident_id, action, timestamp))
    conn.commit()


# ----- EXAMPLE USAGE -----

# Add example users
def add_user(name, role):
    c.execute('INSERT INTO users (name, role) VALUES (?, ?)', (name, role))
    conn.commit()
    return c.lastrowid

# Example
if __name__ == "__main__":
    # Add users
    passenger_id = add_user("Alice", "Passenger")
    driver_id = add_user("Bob", "Driver")
    admin_id = add_user("Charlie", "Admin")
    tc_id = add_user("Dana", "TC")

    # Submit incidents
    submit_incident(passenger_id, "Delay", "Route 101", "Bus late by 15 mins", "Medium")
    submit_incident(driver_id, "Mechanical", "Route 101", "Engine overheating", "High")

    # Monitor incidents
    print("\n--- Monitoring All Incidents ---")
    monitor_incidents()

    # Admin updates status
    update_incident_status(1, "In Progress", assigned_resource="Maintenance Team")

    # Passenger views status
    print("\n--- Passenger Incident Status ---")
    view_incident_status(passenger_id)
