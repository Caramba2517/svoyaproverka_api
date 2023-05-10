from django.urls import path
from api.views import ComplaintList, ComplaintDetail, CustomAuthToken


urlpatterns = [
    path('complaints/', ComplaintList.as_view(), name='complaint_list'),
    path('complaints/<str:pk>/', ComplaintDetail.as_view(), name='complaint_detail'),
    path('user_auntification_token/', CustomAuthToken.as_view())
]
