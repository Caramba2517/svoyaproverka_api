from django.urls import path
from urllib.parse import quote_plus
from api.views import ComplaintList, ComplaintDetail, SearchComplaintsView, SearchComplaintsView_70, \
    SearchPrescriptionsView, SearchPrescriptionsView_70, SearchSolutionsView, SearchSolutionsView_70, SearchAllView, SearchAllView_70, SearchAllView

urlpatterns = [
    path('complaints/', ComplaintList.as_view(), name='complaint_list'),
    path('complaint/<str:pk>/', ComplaintDetail.as_view(), name='complaint_detail'),
    path('complaints/exact/search/<str:query>/', SearchComplaintsView.as_view(), name='search_complaints'),
    path('complaints/inexact/search/<str:query>/', SearchComplaintsView_70.as_view(), name='search_complaints_70'),
    path('solutions/exact/search/<str:query>/', SearchSolutionsView.as_view(), name='search_solutions'),
    path('solutions/inexact/search/<str:query>/', SearchSolutionsView_70.as_view(), name='search_solutions_70'),
    path('prescriptions/exact/search/<str:query>/', SearchPrescriptionsView.as_view(), name='search_prescriptions'),
    path('prescriptions/inexact/search/<str:query>/', SearchPrescriptionsView_70.as_view(),
         name='search_prescriptions_70'),
    path('alldocuments/inexact/search/<str:query>/', SearchAllView_70.as_view(),
         name='search_all_70'),
    path('alldocuments/exact/search/<str:query>/', SearchAllView.as_view(), name='search_all'),
    # path('user_auntification_token/', CustomAuthToken.as_view()),
]
