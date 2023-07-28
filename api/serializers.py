from rest_framework import serializers
from api.models import Complaint
import urllib.parse
from django.urls import reverse
from urllib.parse import quote_plus


class CustomDateTimeField(serializers.ReadOnlyField):
    def to_representation(self, value):
        if value is not None:
            return value.date()
        return None


class ComplaintSerializer(serializers.ModelSerializer):
    list_docs = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [
            'complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name', 'complainant_inn',
            'status', 'numb_purchase', 'justification', 'list_docs', 'json_data'
        ]

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "https://svoyaproverka.ru/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs_str = obj.list_docs[:-1]
        docs = docs_str.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]


class ComplaintsSearchSerializer(serializers.ModelSerializer):
    list_docs = serializers.SerializerMethodField()
    date = CustomDateTimeField()

    class Meta:
        model = Complaint
        fields = ['complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name',
                  'complainant_inn',
                  'status', 'numb_purchase', 'justification', 'list_docs', 'docs_complaints']

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "https://svoyaproverka.ru/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs_str = obj.list_docs[:-1]
        docs = docs_str.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]


class SolutionsSearchSerializer(serializers.ModelSerializer):
    list_docs = serializers.SerializerMethodField()
    date = CustomDateTimeField()

    class Meta:
        model = Complaint
        fields = ['complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name',
                  'complainant_inn',
                  'status', 'numb_purchase', 'justification', 'list_docs', 'docs_solutions']

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "https://svoyaproverka.ru/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs_str = obj.list_docs[:-1]
        docs = docs_str.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]


class PrescriptionsSearchSerializer(serializers.ModelSerializer):
    list_docs = serializers.SerializerMethodField()
    date = CustomDateTimeField()

    class Meta:
        model = Complaint
        fields = ['complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name',
                  'complainant_inn',
                  'status', 'numb_purchase', 'justification', 'list_docs', 'docs_prescriptions']

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "https://svoyaproverka.ru/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs_str = obj.list_docs[:-1]
        docs = docs_str.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]


class AllSearch(serializers.ModelSerializer):
    list_docs = serializers.SerializerMethodField()
    date = CustomDateTimeField()

    class Meta:
        model = Complaint
        fields = ['complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name',
                  'complainant_inn',
                  'status', 'numb_purchase', 'justification', 'list_docs', 'docs_prescriptions', 'docs_solutions',
                  'docs_complaints']

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "https://svoyaproverka.ru/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs_str = obj.list_docs[:-1]
        docs = docs_str.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]
