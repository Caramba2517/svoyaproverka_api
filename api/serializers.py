from rest_framework import serializers
from api.models import Complaint
import urllib.parse


class ComplaintSerializer(serializers.ModelSerializer):
    list_docs = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = '__all__'

    def get_list_docs(self, obj):
        empty_folder = 'Нет файлов'
        site_url = "http://89.108.118.100:8000/file"
        if obj.list_docs == empty_folder:
            return empty_folder
        docs = obj.list_docs.split(";")
        return [f"{site_url}{urllib.parse.quote(doc.strip())}" for doc in docs]
