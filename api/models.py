from django.db import models
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex


class Complaint(models.Model):
    complaint_id = models.CharField(max_length=150, unique=True, primary_key=True)
    status = models.TextField()
    date = models.DateField()
    region = models.TextField()
    customer_name = models.TextField()
    customer_inn = models.TextField(null=True, blank=True)
    complainant_name = models.TextField()
    complainant_inn = models.CharField(max_length=15, null=True, blank=True)
    justification = models.TextField()
    numb_purchase = models.TextField()
    prescription = models.TextField(null=True, blank=True)
    list_docs = models.TextField(null=True, blank=True)
    json_data = models.JSONField()
    docs = models.TextField(null=True, blank=True)
    search_vector = SearchVectorField(null=True, editable=False)

    def save(self, *args, **kwargs):
        self.search_vector = SearchVector('docs')
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'api'
        indexes = [
            GinIndex(fields=['search_vector'])
        ]
