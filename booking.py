from datetime import datetime
import time

# -------------------------
# In-memory "Database"
# -------------------------
users = {
    "admin1": {"role": "Admin"},
    "passenger1": {"role": "Passenger"},
    "driver1": {"role": "Driver"},
    "tc1": {"role": "TC"}
}

trips = {
    101: {"route": "Campus A → Campus B", "total_seats": 5},
}

bookings = []
seat_map = {101: [None] * 5}  # None = available seat


# -------------------------
# Helper Functions
# -------------------------
def send_notification(user, message):
    print(f"[Notification to {user}] {message}")


def check_role(user, allowed_role):
    return users[user]["role"] == allowed_role


# -------------------------
# Passenger Functions
# -------------------------
def reserve_seat(passenger, trip_id):
    seats = seat_map[trip_id]

    for i in range(len(seats)):
        if seats[i] is None:
            seats[i] = passenger
            booking = {
                "passenger": passenger,
                "trip_id": trip_id,
                "seat_number": i + 1,
                "status": "Confirmed",
                "time": datetime.now()
            }
            bookings.append(booking)

            print("Booking successful.")
            print("Ticket Details:", booking)
            return

    print("Error: Seat unavailable.")


def cancel_booking(passenger, trip_id):
    for booking in bookings:
        if booking["passenger"] == passenger and booking["trip_id"] == trip_id:
            booking["status"] = "Cancelled"
            seat_map[trip_id][booking["seat_number"] - 1] = None

            send_notification(passenger, "Your booking has been cancelled.")
            print("Booking cancelled successfully.")
            return

    print("Error: No cancellable booking found.")


def view_booking_history(passenger):
    history = [b for b in bookings if b["passenger"] == passenger]

    if not history:
        print("No booking history available.")
        return

    history.sort(key=lambda x: x["time"])
    for b in history:
        print(b)


# -------------------------
# Admin Functions
# -------------------------
def review_seat_bookings(admin, trip_id):
    if not check_role(admin, "Admin"):
        print("Access denied.")
        return

    print("Seat bookings for trip:", trip_id)
    for booking in bookings:
        if booking["trip_id"] == trip_id:
            print(booking)


def modify_booking(admin, passenger, trip_id, action):
    if not check_role(admin, "Admin"):
        print("Access denied.")
        return

    for booking in bookings:
        if booking["passenger"] == passenger and booking["trip_id"] == trip_id:
            if action == "Cancel":
                booking["status"] = "Cancelled"
                seat_map[trip_id][booking["seat_number"] - 1] = None
                send_notification(passenger, "Admin cancelled your booking.")
            else:
                print("Modify booking logic goes here.")

            print("Admin action successful.")
            return

    print("Error: Booking not found.")


# -------------------------
# Driver Seat Occupancy
# -------------------------
def view_seat_occupancy_driver(driver, trip_id):
    if not check_role(driver, "Driver"):
        print("Access denied.")
        return

    seats = seat_map[trip_id]
    booked = sum(1 for s in seats if s)
    available = len(seats) - booked

    print(f"Seat Occupancy: {booked}/{len(seats)} booked, {available} available")
    print("Booked seat numbers:",
          [i + 1 for i, s in enumerate(seats) if s])


# -------------------------
# Transport Coordinator Dashboard
# -------------------------
def view_seat_occupancy_tc(tc):
    if not check_role(tc, "TC"):
        print("Access denied.")
        return

    for trip_id, seats in seat_map.items():
        booked = sum(1 for s in seats if s)
        total = len(seats)

        print(f"Trip {trip_id}: {booked}/{total} occupied")

        if booked / total > 0.8:
            print("⚠ Overcrowded trip detected")
        elif booked / total < 0.3:
            print("ℹ Underutilised trip")


# -------------------------
# Demo Execution
# -------------------------
reserve_seat("passenger1", 101)
reserve_seat("passenger1", 101)

view_booking_history("passenger1")

review_seat_bookings("admin1", 101)
modify_booking("admin1", "passenger1", 101, "Cancel")

view_seat_occupancy_driver("driver1", 101)
view_seat_occupancy_tc("tc1")
