import time
import random
from threading import Thread

# -----------------------------
# Shuttle Model
# -----------------------------
class Shuttle:
    def __init__(self, shuttle_id, route):
        self.shuttle_id = shuttle_id
        self.route = route
        self.lat = 3.1390      # starting GPS (example)
        self.lon = 101.6869
        self.status = "On Trip"
        self.gps_active = True

    def update_location(self):
        if not self.gps_active:
            raise Exception("GPS unavailable")

        # Simulate movement (within ~10 meters)
        self.lat += random.uniform(-0.00005, 0.00005)
        self.lon += random.uniform(-0.00005, 0.00005)

    def calculate_eta(self):
        return random.randint(2, 15)  # ETA in minutes


# -----------------------------
# System Functions
# -----------------------------
def retrieve_gps(shuttle):
    if not shuttle.gps_active:
        raise Exception("Unable to retrieve shuttle location")
    return shuttle.lat, shuttle.lon


def display_shuttle_info(user, shuttle):
    try:
        lat, lon = retrieve_gps(shuttle)
        eta = shuttle.calculate_eta()
        print(f"[{user}] Shuttle {shuttle.shuttle_id}")
        print(f" Location: ({lat:.6f}, {lon:.6f})")
        print(f" Status: {shuttle.status}")
        print(f" ETA: {eta} minutes\n")
    except Exception as e:
        print(f"[ERROR] {e}\n")


# -----------------------------
# Driver Updates Location
# -----------------------------
def driver_update(shuttle):
    while True:
        try:
            shuttle.update_location()
            print("[Driver] Location updated successfully")
        except Exception as e:
            print("[Driver ALERT]", e)
        time.sleep(5)  # refresh every 5 seconds


# -----------------------------
# Admin / Passenger / TC View
# -----------------------------
def live_tracking(user, shuttle, refresh_time):
    while True:
        display_shuttle_info(user, shuttle)
        time.sleep(refresh_time)


# -----------------------------
# Main Simulation
# -----------------------------
shuttle1 = Shuttle("SH01", "Route A")

# Start driver GPS updates
Thread(target=driver_update, args=(shuttle1,), daemon=True).start()

# Different user views
Thread(target=live_tracking, args=("Admin", shuttle1, 5), daemon=True).start()
Thread(target=live_tracking, args=("Passenger", shuttle1, 5), daemon=True).start()
Thread(target=live_tracking, args=("Transport Coordinator", shuttle1, 10), daemon=True).start()

# Keep program running
while True:
    time.sleep(1)
