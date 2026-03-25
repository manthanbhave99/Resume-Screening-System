from database import add_user, check_user, create_users_table

create_users_table()


def check_login(username, password):
    # Admin login
    if username == "admin" and password == "VM@1917":
        return True, "admin"

    # Normal user login
    if check_user(username, password):
        return True, "user"

    return False, None


def signup_user(username, password):
    if not username or not password:
        return False, "Username and password cannot be empty"

    success = add_user(username, password)

    if success:
        return True, "Signup successful"
    else:
        return False, "Username already exists"
