# ==========================================
# Simulated Database
# ==========================================
users_db = []

# ==========================================
# User Model
# ==========================================
class User:
    def __init__(self, user_id, full_name, email, password, role, status="Active"):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.password = password   # plain text
        self.role = role
        self.status = status

# ==========================================
# Utility Functions
# ==========================================
def is_admin(user):
    return user.role == "Admin"

def is_duplicate(email, user_id):
    for user in users_db:
        if user.email == email or user.user_id == user_id:
            return True
    return False

def validate_registration_input(full_name, user_id, email, password):
    if not full_name or not email or not password or not user_id:
        return False, "All fields are required."

    if "@" not in email:
        return False, "Invalid email format."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    return True, "Validation successful."

# ==========================================
# Registration (Passenger / Driver / TC)
# ==========================================
def register_account(full_name, user_id, email, password, role):
    allowed_roles = ["Passenger", "Driver", "TC"]

    if role not in allowed_roles:
        return "Error: This role cannot self-register."

    valid, message = validate_registration_input(full_name, user_id, email, password)
    if not valid:
        return f"Error: {message}"

    if is_duplicate(email, user_id):
        return "Error: Email or ID already exists."

    try:
        new_user = User(
            user_id=user_id,
            full_name=full_name,
            email=email,
            password=password,
            role=role
        )
        users_db.append(new_user)
        return f"{role} registered successfully. Redirecting to login page..."

    except Exception:
        return "Error: Database error occurred."

# ==========================================
# Admin Creates Admin Account
# ==========================================
def create_admin_account(admin, full_name, user_id, email, password):
    if not is_admin(admin):
        return "Access denied: Admin only."

    if is_duplicate(email, user_id):
        return "Error: Email or ID already exists."

    new_admin = User(
        user_id=user_id,
        full_name=full_name,
        email=email,
        password=password,
        role="Admin"
    )
    users_db.append(new_admin)

    return "Admin account created successfully."

# ==========================================
# Admin: View All Users
# ==========================================
def view_all_users(admin):
    if not is_admin(admin):
        return "Access denied: Admin only."

    print("\n--- User List ---")
    for user in users_db:
        print(f"ID: {user.user_id}, Name: {user.full_name}, "
              f"Email: {user.email}, Role: {user.role}, Status: {user.status}")

# ==========================================
# Admin: Update User (Email / Role)
# ==========================================
def update_user(admin, user_id, new_email=None, new_role=None):
    if not is_admin(admin):
        return "Access denied: Admin only."

    for user in users_db:
        if user.user_id == user_id:
            if new_email and any(u.email == new_email for u in users_db if u.user_id != user_id):
                return "Error: Duplicate email detected."

            if new_email:
                user.email = new_email
            if new_role:
                user.role = new_role

            return "User updated successfully."

    return "Error: User not found."

# ==========================================
# Admin: Deactivate / Reactivate Account
# ==========================================
def update_account_status(admin, user_id, status):
    if not is_admin(admin):
        return "Access denied: Admin only."

    for user in users_db:
        if user.user_id == user_id:
            user.status = status
            return f"Account status updated to {status}."

    return "Error: User not found."

# ==========================================
# Demo / Testing
# ==========================================

# System creates first Admin
system_admin = User(1, "System Admin", "admin@system.com", "admin123", "Admin")
users_db.append(system_admin)

# Self-registration
print(register_account("Ali Ahmad", 2, "ali@email.com", "password123", "Passenger"))
print(register_account("Siti Driver", 3, "driver@email.com", "driver123", "Driver"))
print(register_account("Ahmad TC", 4, "tc@email.com", "tcpass123", "TC"))

# Admin actions
view_all_users(system_admin)
print(update_user(system_admin, 2, new_role="TC"))
print(update_account_status(system_admin, 3, "Inactive"))

# Admin creates another admin
print(create_admin_account(system_admin, "Second Admin", 5, "admin2@system.com", "adminpass"))
view_all_users(system_admin)
