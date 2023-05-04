from django_filters import rest_framework as filters
from api.models import Complaint


class ComplaintFilter(filters.FilterSet):
    complaint_id = filters.CharFilter(label='Уникальный ID жалобы')
    date = filters.DateFilter(label='Дата')
    region = filters.MultipleChoiceFilter(label='Подразделение ФАС')
    customer_name = filters.CharFilter(label='Имя заказчика', lookup_expr='icontains')
    customer_inn = filters.CharFilter(label='ИНН заказчика')
    complainant_name = filters.CharFilter(label='Имя жалобщика', lookup_expr='icontains')
    complainant_inn = filters.CharFilter(label='ИНН жалобщика')
    status = filters.MultipleChoiceFilter(label='Статус жалобы')
    numb_purchase = filters.CharFilter(label="Номер закупки")
    justification = filters.MultipleChoiceFilter(label="Результат рассмотрения")

    class Meta:
        model = Complaint
        fields = [
            'complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name', 'complainant_inn',
            'status', 'numb_purchase', 'justification'
        ]
