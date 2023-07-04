from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry
from api.models import Complaint


@receiver([post_save, post_delete], sender=Complaint)
def update_complaint_index(sender, instance, **kwargs):
    for document in registry.get_documents():
        document.update(instance)