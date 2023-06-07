from django.urls import path, include
from api.views import serve_file
from svoyaproverka_api.yasg import urlpatterns as swagger_urls
from api.views import redirect_to_api_v1

urlpatterns = [
    path('', redirect_to_api_v1),
    path('api/v2/', include('api.urls')),
    path('file/<path:file_path>/', serve_file, name='serve_file')
 ]

urlpatterns += swagger_urls
