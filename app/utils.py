from django.db import transaction
from django.apps import apps

def handle_delete_request(id, fk):
    try:
        with transaction.atomic():
            for model_class in apps.get_models():
                if hasattr(model_class, fk):
                    related_objects = model_class.objects.filter(**{fk: id})
                    related_objects.update(is_deleted=True)
        return True
    except:
        return False
    
    
    
         