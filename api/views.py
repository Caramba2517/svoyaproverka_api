from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from api.models import Complaint
from api.serializers import ComplaintSerializer
from api.filters import ComplaintFilter
import os
from django.http import FileResponse
from django.shortcuts import redirect
from rest_framework.pagination import LimitOffsetPagination


def redirect_to_api_v1(request):
    return redirect('http://89.108.118.100:8000/api/v1/complaints/?limit=10')


def serve_file(request, file_path):
    full_file_path = os.path.join('/', file_path)
    file = open(full_file_path, 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(full_file_path))
    return response


class ComplaintList(generics.ListAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComplaintFilter
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 2
    pagination_class.max_limit = 1000


class ComplaintDetail(generics.RetrieveAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    lookup_field = 'pk'
