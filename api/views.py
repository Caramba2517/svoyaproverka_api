from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.models import Complaint
from api.serializers import ComplaintSerializer, ComplaintsSearchSerializer, SolutionsSearchSerializer, PrescriptionsSearchSerializer
from api.filters import ComplaintFilter
import os
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from api.documents import ComplaintsDocument, SolutionsDocument, PrescriptionsDocument
from elasticsearch_dsl import Q
from urllib.parse import quote_plus, urlencode



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

    def get_object(self):
        pk = quote_plus(self.kwargs['pk'])
        return self.queryset.get(pk=pk)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class SearchComplaintsView(APIView):
    productinventory_serializer = ComplaintsSearchSerializer
    search_document = ComplaintsDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=["docs_complaints"]
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            size = int(request.GET.get('size', 10))
            from_value = int(request.GET.get('from', 0))
            search = search.extra(size=size, from_=from_value, track_total_hits=True)
            response = search.execute()
            results = response.hits
            serializer = self.productinventory_serializer(results, many=True)
            next_link = None
            previous_link = None
            if from_value + size < response.hits.total.value:
                params = {
                    'size': str(size),
                    'from': str(from_value + size)
                }
                next_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            if from_value - size >= 0:
                params = {
                    'size': str(size),
                    'from': str(max(from_value - size, 0))
                }
                previous_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            data = {
                'count': response.hits.total,
                'next': next_link,
                'previous': previous_link,
                'results': serializer.data
            }
            return Response(data)
        except Exception as e:
            return HttpResponse(str(e), status=500)


class SearchComplaintsView_70(APIView, LimitOffsetPagination):
    productinventory_serializer = ComplaintsSearchSerializer
    search_document = ComplaintsDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=["docs_complaints"],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            size = int(request.GET.get('size', 10))
            from_value = int(request.GET.get('from', 0))
            search = search.extra(size=size, from_=from_value, track_total_hits=True)
            response = search.execute()
            results = response.hits
            serializer = self.productinventory_serializer(results, many=True)
            next_link = None
            previous_link = None
            if from_value + size < response.hits.total.value:
                params = {
                    'size': str(size),
                    'from': str(from_value + size)
                }
                next_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            if from_value - size >= 0:
                params = {
                    'size': str(size),
                    'from': str(max(from_value - size, 0))
                }
                previous_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            data = {
                'count': response.hits.total,
                'next': next_link,
                'previous': previous_link,
                'results': serializer.data
            }
            return Response(data)
        except Exception as e:
            return HttpResponse(str(e), status=500)


class SearchSolutionsView(APIView, LimitOffsetPagination):
    productinventory_serializer = SolutionsSearchSerializer
    search_document = SolutionsDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=["docs_complaints"]
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            size = int(request.GET.get('size', 10))
            from_value = int(request.GET.get('from', 0))
            search = search.extra(size=size, from_=from_value, track_total_hits=True)
            response = search.execute()
            results = response.hits
            serializer = self.productinventory_serializer(results, many=True)
            next_link = None
            previous_link = None
            if from_value + size < response.hits.total.value:
                params = {
                    'size': str(size),
                    'from': str(from_value + size)
                }
                next_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            if from_value - size >= 0:
                params = {
                    'size': str(size),
                    'from': str(max(from_value - size, 0))
                }
                previous_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            data = {
                'count': response.hits.total,
                'next': next_link,
                'previous': previous_link,
                'results': serializer.data
            }
            return Response(data)
        except Exception as e:
            return HttpResponse(str(e), status=500)


class SearchSolutionsView_70(APIView, LimitOffsetPagination):
    productinventory_serializer = SolutionsSearchSerializer
    search_document = SolutionsDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=["docs_complaints"],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            size = int(request.GET.get('size', 10))
            from_value = int(request.GET.get('from', 0))
            search = search.extra(size=size, from_=from_value, track_total_hits=True)
            response = search.execute()
            results = response.hits
            serializer = self.productinventory_serializer(results, many=True)
            next_link = None
            previous_link = None
            if from_value + size < response.hits.total.value:
                params = {
                    'size': str(size),
                    'from': str(from_value + size)
                }
                next_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            if from_value - size >= 0:
                params = {
                    'size': str(size),
                    'from': str(max(from_value - size, 0))
                }
                previous_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            data = {
                'count': response.hits.total,
                'next': next_link,
                'previous': previous_link,
                'results': serializer.data
            }
            return Response(data)
        except Exception as e:
            return HttpResponse(str(e), status=500)


class SearchPrescriptionsView(APIView, LimitOffsetPagination):
    productinventory_serializer = PrescriptionsSearchSerializer
    search_document = PrescriptionsDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=["docs_complaints"]
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            size = int(request.GET.get('size', 10))
            from_value = int(request.GET.get('from', 0))
            search = search.extra(size=size, from_=from_value, track_total_hits=True)
            response = search.execute()
            results = response.hits
            serializer = self.productinventory_serializer(results, many=True)
            next_link = None
            previous_link = None
            if from_value + size < response.hits.total.value:
                params = {
                    'size': str(size),
                    'from': str(from_value + size)
                }
                next_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            if from_value - size >= 0:
                params = {
                    'size': str(size),
                    'from': str(max(from_value - size, 0))
                }
                previous_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            data = {
                'count': response.hits.total,
                'next': next_link,
                'previous': previous_link,
                'results': serializer.data
            }
            return Response(data)
        except Exception as e:
            return HttpResponse(str(e), status=500)


class SearchPrescriptionsView_70(APIView, LimitOffsetPagination):
    productinventory_serializer = PrescriptionsSearchSerializer
    search_document = PrescriptionsDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=["docs_complaints"],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            size = int(request.GET.get('size', 10))
            from_value = int(request.GET.get('from', 0))
            search = search.extra(size=size, from_=from_value, track_total_hits=True)
            response = search.execute()
            results = response.hits
            serializer = self.productinventory_serializer(results, many=True)
            next_link = None
            previous_link = None
            if from_value + size < response.hits.total.value:
                params = {
                    'size': str(size),
                    'from': str(from_value + size)
                }
                next_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            if from_value - size >= 0:
                params = {
                    'size': str(size),
                    'from': str(max(from_value - size, 0))
                }
                previous_link = request.build_absolute_uri('?{}'.format(urlencode(params)))
            data = {
                'count': response.hits.total,
                'next': next_link,
                'previous': previous_link,
                'results': serializer.data
            }
            return Response(data)
        except Exception as e:
            return HttpResponse(str(e), status=500)
