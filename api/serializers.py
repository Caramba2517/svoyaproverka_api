from rest_framework import serializers
from api.models import Complaint
import urllib.parse
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
        site_url = "http://89.108.118.100:8000/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs_str = obj.list_docs[:-1]
        docs = docs_str.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]


class ComplaintsSearchSerializer(serializers.ModelSerializer):
    complaint_id = serializers.SerializerMethodField()
    list_docs = serializers.SerializerMethodField()
    date = CustomDateTimeField()

    class Meta:
        model = Complaint
        fields = ['complaint_id', 'date', 'region', 'customer_name', 'customer_inn', 'complainant_name',
                  'complainant_inn',
                  'status', 'numb_purchase', 'justification', 'list_docs', 'docs_complaints']

    def get_complaint_id(self, obj):
        return f"https://svoyaproverka.ru/api/v2/complaint/{quote_plus(obj.complaint_id)}"

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "http://89.108.118.100:8000/file"
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
                  'status', 'numb_purchase', 'justification', 'list_docs', 'docs_complaints']

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "http://89.108.118.100:8000/file"
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
                  'status', 'numb_purchase', 'justification', 'list_docs', 'docs_complaints']

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "http://89.108.118.100:8000/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs_str = obj.list_docs[:-1]
        docs = docs_str.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]
