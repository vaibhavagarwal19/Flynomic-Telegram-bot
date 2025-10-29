from .api_client import post

def register_user(first_name, last_name, email, phone):
    """Registers a new user via the backend API."""
    data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phoneNumber": phone or ""
    }
    return post("users/register", data)


def resend_otp(first_name, last_name, email, phone):
    """Requests a new OTP for login (same as registration fields)."""
    data = {
        "firstName": first_name or "",
        "lastName": last_name or "",
        "email": email,
        "phoneNumber": phone or ""
    }
    return post("users/resend-otp", data)


def verify_otp(email, otp):
    """Verifies OTP for login/registration."""
    data = {
        "email": email,
        "otp": otp
    }
    return post("auth/register-otp-verify", data)
