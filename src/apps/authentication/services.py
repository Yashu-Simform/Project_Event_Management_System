from src.apps.authentication.models import EmsUser
def get_user(id):
    try:
        user = EmsUser.objects.get(id=id)
        return user
    except:
        return None