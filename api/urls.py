from django.urls import path
from api.views import ComplaintList, ComplaintDetail


urlpatterns = [
    path('complaints/', ComplaintList.as_view(), name='complaint_list'),
    path('complaints/<str:pk>/', ComplaintDetail.as_view(), name='complaint_detail'),
]
