from django.db import models


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

    class Meta:
        app_label = 'api'
