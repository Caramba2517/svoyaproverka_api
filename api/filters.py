from django_filters import rest_framework as filters
from api.models import Complaint

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from svoyaproverka_api import settings


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

    docs_complaints = filters.CharFilter(method='search_docs_complaints',
                                         label='Поиск по жалобам (точное совпадение)')
    docs_solutions = filters.CharFilter(method='search_docs_solutions',
                                        label='Поиск по решениям (точное совпадение)')
    docs_prescriptions = filters.CharFilter(method='search_docs_prescriptions',
                                            label='Поиск по предписаниям (точное совпадение)')
    docs_complaints_2 = filters.CharFilter(method='search_docs_complaints_2',
                                           label='Поиск по жалобам (сходство более 70%)')
    docs_solutions_2 = filters.CharFilter(method='search_docs_solutions_2',
                                          label='Поиск по решениям (сходство более 70%)')
    docs_prescriptions_2 = filters.CharFilter(method='search_docs_prescriptions_2',
                                              label='Поиск по предписаниям (сходство более 70%)')

    def search_docs_complaints(self, queryset, name, value, page_number=1, page_size=10):
        client = Elasticsearch(timeout=60)
        s = Search(using=client, index='complaints')
        s = s.query('match_phrase', docs_complaints=value)
        s = s[0:10000]
        response = s.execute()
        complaint_ids = [hit.meta.id for hit in response.hits]
        queryset = queryset.filter(complaint_id__in=complaint_ids)
        return queryset

    def search_docs_complaints_2(self, queryset, name, value):
        client = Elasticsearch(timeout=60)
        s = Search(using=client, index='complaints')
        s = s.query('match_phrase', docs_complaints={
            'query': value,
            'slop': 2
        })
        s = s[0:10000]
        response = s.execute()
        complaint_ids = [hit.meta.id for hit in response.hits]
        queryset = queryset.filter(complaint_id__in=complaint_ids)
        return queryset

    def search_docs_solutions(self, queryset, name, value):
        client = Elasticsearch(timeout=60)
        s = Search(using=client, index='solutions')
        s = s.query('match_phrase', docs_solutions=value)
        s = s[0:10000]
        response = s.execute()
        complaint_ids = [hit.meta.id for hit in response.hits]
        queryset = queryset.filter(complaint_id__in=complaint_ids)
        return queryset

    def search_docs_solutions_2(self, queryset, name, value):
        client = Elasticsearch(timeout=60)
        s = Search(using=client, index='solutions')
        s = s.query('match_phrase', docs_solutions={
            'query': value,
            'slop': 2
        })
        s = s[0:10000]
        response = s.execute()
        complaint_ids = [hit.meta.id for hit in response.hits]
        queryset = queryset.filter(complaint_id__in=complaint_ids)
        return queryset

    def search_docs_prescriptions(self, queryset, name, value):
        client = Elasticsearch(timeout=60)
        s = Search(using=client, index='prescriptions')
        s = s.query('match_phrase', docs_prescriptions=value)
        s = s[0:10000]
        response = s.execute()
        complaint_ids = [hit.meta.id for hit in response.hits]
        queryset = queryset.filter(complaint_id__in=complaint_ids)
        return queryset

    def search_docs_prescriptions_2(self, queryset, name, value):
        client = Elasticsearch(timeout=60)
        s = Search(using=client, index='prescriptions')
        s = s.query('match_phrase', docs_prescriptions={
            'query': value,
            'slop': 2
        })
        s = s[0:10000]
        response = s.execute()
        complaint_ids = [hit.meta.id for hit in response.hits]
        queryset = queryset.filter(complaint_id__in=complaint_ids)
        return queryset

    class Meta:
        model = Complaint
        fields = [
            'complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name', 'complainant_inn',
            'status', 'numb_purchase', 'justification', 
        ]
