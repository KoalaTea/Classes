from functools import wraps
from flask import abort
from flask_login import current_user

# Roles
# admin - access to everything
# bartender - access to anything alchohol related
# user - access to menu and ordering

def permission_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            hasrole = False
            for role in roles:
                if current_user.is_role(role):
                    hasrole = True
            if not hasrole:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(['admin'])(f)

#Admin has permissions to everything.
def bartender_required(f):
    return permission_required(['admin','bartender'])(f)
