import os

from django_filters import rest_framework as filters
from api.models import Complaint


class ComplaintFilter(filters.FilterSet):
    complaint_id = filters.CharFilter(label='Уникальный ID жалобы')
    date = filters.DateFromToRangeFilter(label='Дата')
    region = filters.ChoiceFilter(
        label='Подразделение ФАС',
        choices=[(region, region) for region in
                 Complaint.objects.order_by('region').values_list('region', flat=True).distinct()])
    customer_name = filters.CharFilter(label='Имя заказчика', lookup_expr='icontains')
    customer_inn = filters.CharFilter(label='ИНН заказчика')
    complainant_name = filters.CharFilter(label='Имя жалобщика', lookup_expr='icontains')
    complainant_inn = filters.CharFilter(label='ИНН жалобщика')
    status = filters.MultipleChoiceFilter(
        label='Статус жалобы',
        choices=[(status, status) for status in
                 Complaint.objects.order_by().values_list('status', flat=True).distinct()])
    numb_purchase = filters.CharFilter(label="Номер закупки")
    justification = filters.MultipleChoiceFilter(
        label="Результат рассмотрения",
        choices=[(justification, justification) for justification in
                 Complaint.objects.order_by().values_list('justification', flat=True).distinct()])
    docs = filters.CharFilter(label='Поиск по ключевым словам', lookup_expr='icontains')

    class Meta:
        model = Complaint
        fields = [
            'complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name', 'complainant_inn',
            'status', 'numb_purchase', 'justification', 'docs',
        ]
        search_fields = ['docs']
