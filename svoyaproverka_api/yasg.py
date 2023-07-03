from rest_framework import permissions
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Svoya-Proverka API",
        default_version='v2.0',
        description="API предназначен для быстрого поиска и проверки жалоб и бла-бла...",
        contact=openapi.Contact(email="caramba.ge@yandex.ru"),
        license=openapi.License(name="Svoya-proverka API"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('documentation/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('documentation/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
