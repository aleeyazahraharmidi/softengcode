import datetime
import random
import pandas as pd

# Mock database data
users = [
    {"user_id": 1, "role": "Admin", "email": "admin@example.com"},
    {"user_id": 2, "role": "Passenger", "email": "passenger@example.com"},
    {"user_id": 3, "role": "Driver", "email": "driver@example.com"},
]

trips = [
    {"trip_id": 101, "passenger_id": 2, "driver_id": 3, "date": "2026-01-20", "status": "Completed"},
    {"trip_id": 102, "passenger_id": 2, "driver_id": 3, "date": "2026-01-21", "status": "Completed"},
    {"trip_id": 103, "passenger_id": 2, "driver_id": 3, "date": "2026-01-25", "status": "Scheduled"},
]

incidents = [
    {"trip_id": 101, "driver_id": 3, "resolved": True},
    {"trip_id": 102, "driver_id": 3, "resolved": False},
]

# Base class for dashboards
class Dashboard:
    def __init__(self, user_id):
        self.user_id = user_id

    def retrieve_data(self):
        raise NotImplementedError

    def display(self):
        raise NotImplementedError

# Admin Reports and Analytics
class AdminDashboard(Dashboard):
    def retrieve_data(self, start_date=None, end_date=None):
        if not start_date:
            start_date = datetime.date.today() - datetime.timedelta(days=30)
        if not end_date:
            end_date = datetime.date.today()

        # Filter trips within date range
        filtered_trips = [t for t in trips if start_date <= datetime.date.fromisoformat(t["date"]) <= end_date]

        if not filtered_trips:
            raise ValueError("No data available for selected parameters")
        return filtered_trips

    def generate_report(self, start_date=None, end_date=None):
        data = self.retrieve_data(start_date, end_date)
        df = pd.DataFrame(data)
        report = df.groupby("driver_id").agg({"trip_id": "count"})
        print("\nAdmin Report: Trip counts by driver\n", report)
        return report

    def export_report(self, report, filename="report.pdf"):
        # Simulated PDF export
        report.to_csv(filename.replace(".pdf", ".csv"))
        print(f"Report exported as {filename}")

# Passenger Dashboard
class PassengerDashboard(Dashboard):
    def retrieve_data(self):
        passenger_trips = [t for t in trips if t["passenger_id"] == self.user_id]
        if not passenger_trips:
            raise ValueError("No trip data available")
        return passenger_trips

    def display(self):
        data = self.retrieve_data()
        upcoming = [t for t in data if t["status"] == "Scheduled"]
        history = [t for t in data if t["status"] == "Completed"]
        print(f"\nPassenger Dashboard\nUpcoming trips: {upcoming}\nTravel history: {history}")

# Driver Performance Dashboard
class DriverDashboard(Dashboard):
    def retrieve_data(self):
        driver_trips = [t for t in trips if t["driver_id"] == self.user_id and t["status"] == "Completed"]
        if not driver_trips:
            return None
        return driver_trips

    def display(self):
        data = self.retrieve_data()
        if not data:
            print("No performance data")
            return

        total_trips = len(data)
        incidents_resolved = sum(1 for i in incidents if i["driver_id"] == self.user_id and i["resolved"])
        incidents_unresolved = total_trips - incidents_resolved
        on_time_rate = round(random.uniform(85, 100), 2)  # Mock on-time percentage

        print(f"\nDriver Performance Dashboard\nTotal trips: {total_trips}")
        print(f"On-time rate: {on_time_rate}%")
        print(f"Resolved incidents: {incidents_resolved}, Unresolved: {incidents_unresolved}")

# Example usage
if __name__ == "__main__":
    # Admin
    admin_dash = AdminDashboard(user_id=1)
    report = admin_dash.generate_report()
    admin_dash.export_report(report)

    # Passenger
    passenger_dash = PassengerDashboard(user_id=2)
    passenger_dash.display()

    # Driver
    driver_dash = DriverDashboard(user_id=3)
    driver_dash.display()
