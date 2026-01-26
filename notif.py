import time
import random
from datetime import datetime

# -----------------------------
# User Classes
# -----------------------------
class User:
    def __init__(self, user_id, role, notifications_enabled=True):
        self.user_id = user_id
        self.role = role
        self.notifications_enabled = notifications_enabled
        self.inbox = []

    def receive_notification(self, message):
        if self.notifications_enabled:
            self.inbox.append(message)
            return True
        return False


# -----------------------------
# Notification System
# -----------------------------
class NotificationSystem:
    def __init__(self):
        self.delivery_log = []

    def send_notification(self, users, message, channel="App"):
        failed_users = []

        for user in users:
            delivered = user.receive_notification(message)
            if delivered:
                self.delivery_log.append(
                    f"{datetime.now()} | Delivered to {user.user_id} via {channel}"
                )
            else:
                failed_users.append(user.user_id)

        return failed_users

    def broadcast(self, users, message):
        print("Broadcasting notification...")
        failed = self.send_notification(users, message)

        if not failed:
            print("✔ Broadcast successful")
        else:
            print("⚠ Broadcast partially failed")
            print("Users not reached:", failed)

    def log_status(self):
        print("\n--- Notification Log ---")
        for log in self.delivery_log:
            print(log)


# -----------------------------
# Admin: Broadcast Notification
# -----------------------------
def admin_broadcast(admin, system, users):
    print("\n[Admin] Broadcasting Notification")

    message = "Shuttle service will be delayed by 15 minutes."
    target_users = users  # all users

    failed_users = system.send_notification(target_users, message)

    if not failed_users:
        print("✔ Admin notified all users successfully")
    else:
        print("⚠ Notification failed for:", failed_users)


# -----------------------------
# Passenger: Receive Shuttle Alerts
# -----------------------------
def shuttle_event_alert(system, passenger, event_type):
    print("\n[System] Detecting shuttle event...")

    alert_map = {
        "confirmation": "Your shuttle booking is confirmed.",
        "delay": "Shuttle delayed due to traffic.",
        "cancellation": "Shuttle service has been cancelled."
    }

    message = alert_map.get(event_type, "Shuttle update available.")
    success = passenger.receive_notification(message)

    if success:
        print("✔ Passenger received real-time alert")
    else:
        print("⚠ Push failed — displaying fallback banner")


# -----------------------------
# Driver: Route / Schedule Updates
# -----------------------------
def driver_route_update(system, driver):
    print("\n[System] Route/Schedule Updated")

    message = "Route A updated. New start time: 8:30 AM."
    success = driver.receive_notification(message)

    if success:
        print("✔ Driver informed in real time")
    else:
        print("⚠ Notification failed — saved to Notifications tab")


# -----------------------------
# Transport Coordinator: Send Notification
# -----------------------------
def coordinator_send_notification(system, coordinator, users):
    print("\n[Transport Coordinator] Sending Notification")

    message = "Reminder: Morning shuttle starts at 7:00 AM."
    scheduled = False  # immediate delivery

    if scheduled:
        print("Notification scheduled")
        time.sleep(2)

    failed_users = system.send_notification(users, message, channel="Email")

    if failed_users:
        print("⚠ Some recipients did not receive notification:", failed_users)
    else:
        print("✔ Notification delivered to all recipients")


# -----------------------------
# Simulation
# -----------------------------
if __name__ == "__main__":
    # Create users
    admin = User(1, "Admin")
    passenger = User(2, "Passenger")
    driver = User(3, "Driver")
    coordinator = User(4, "Transport Coordinator")

    users = [passenger, driver, coordinator]

    # Initialize system
    notification_system = NotificationSystem()

    # Admin broadcast
    admin_broadcast(admin, notification_system, users)

    # Passenger alert
    shuttle_event_alert(notification_system, passenger, "delay")

    # Driver update
    driver_route_update(notification_system, driver)

    # Coordinator notification
    coordinator_send_notification(notification_system, coordinator, users)

    # View logs
    notification_system.log_status()
