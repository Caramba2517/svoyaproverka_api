from django.db import models


class Complaint(models.Model):
    complaint_id = models.CharField(max_length=150, unique=True, primary_key=True)
    status = models.CharField(max_length=150)
    date = models.DateField()
    region = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=200)
    customer_inn = models.CharField(max_length=15, null=True, blank=True)
    complainant_name = models.CharField(max_length=200)
    complainant_inn = models.CharField(max_length=15, null=True, blank=True)
    justification = models.TextField()
    numb_purchase = models.CharField(max_length=150)
    prescription = models.TextField(null=True, blank=True)
    list_docs = models.TextField(null=True, blank=True)
    json_data = models.JSONField()

    class Meta:
        app_label = 'api'
