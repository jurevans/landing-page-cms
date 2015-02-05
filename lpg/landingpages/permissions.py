
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

def get_perm(Model, perm):
    '''
    Return the permission object, for the Model
    '''
    ct = ContentType.objects.get_for_model(Model)
    return Permission.objects.get(content_type=ct,codename=perm)

