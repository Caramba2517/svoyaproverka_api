import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.models import Complaint
from api.serializers import ComplaintSerializer
from api.filters import ComplaintFilter
import os
from django.http import FileResponse
from django.shortcuts import redirect
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from api.documents import ComplaintsDocument, SolutionsDocument, PrescriptionsDocument
from elasticsearch_dsl import Q


def redirect_to_api_v1(request):
    return redirect('http://89.108.118.100:8000/api/v1/complaints/?limit=10')


def serve_file(request, file_path):
    full_file_path = os.path.join('/', file_path)
    file = open(full_file_path, 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(full_file_path))
    return response


class ComplaintList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Complaint.objects.all().order_by('-date')
    serializer_class = ComplaintSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComplaintFilter
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10
    pagination_class.max_limit = 20


class ComplaintDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Complaint.objects.all().order_by('-date')
    serializer_class = ComplaintSerializer
    lookup_field = 'pk'


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

