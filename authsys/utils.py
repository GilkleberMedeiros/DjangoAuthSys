from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.contrib.auth.models import Permission


# Utilities func for Permissions
def is_permission_created(
        permission_codename: str, 
        permission_name: str = None, 
        model_or_contentType: Model | ContentType = None
        ) -> Permission | bool:
    if model_or_contentType is not None:
        model_or_contentType = get_content_type_from_model(model_or_contentType)
    
    try: 
        perm = Permission.objects.get(
        codename=permission_codename, 
        name=permission_name,
        content_type=model_or_contentType
        )
    except: return False

    return perm

def get_content_type_from_model(model: Model | ContentType) -> ContentType:
    content_type = model
    if not issubclass(model.__class__, ContentType):
        content_type = ContentType.objects.get_for_model(model)
    
    return content_type

def create_permission(codename: str, name: str, model_or_contentType: Model | ContentType) -> Permission:
    content_type = get_content_type_from_model(model_or_contentType)

    permission = Permission.objects.create(
        codename=codename,
        name=name,
        content_type=content_type,
    )

    return permission

def is_permission_created_create(codename: str, name: str, model_or_contentType: Model | ContentType) -> Permission:
    if not (perm_or_false := is_permission_created(codename, 
        permission_name=name, 
        model_or_contentType=model_or_contentType)):
        perm = create_permission(codename, name, model_or_contentType)

        return perm
    
    return perm_or_false