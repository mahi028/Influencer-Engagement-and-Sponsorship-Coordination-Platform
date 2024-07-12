from application.modals import UserRoles

def user_roles(user_id):
    roles = UserRoles.query.filter_by(user_id = user_id).all()
    available_roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
    user_roles = [available_roles[role.role_id] for role in roles]
    return user_roles

def is_admin(user_id):
    if 'Admin' in user_roles(user_id):
        return True
    return False