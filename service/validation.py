from service import user


def validate_login(found_user, password):
    errors = {}
    if found_user is None:
        errors["phone"] = "No such user"
        return errors
    is_correct_password = user.check_user_password(found_user, password)
    if not is_correct_password:
        errors["password"] = "Incorrect password"
    return errors
