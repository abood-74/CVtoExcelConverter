from django.urls import path

from . import views

urlpatterns = [
    path('cv/upload/', views.CVUploadView.as_view(), name='cv_upload'),
    path('cv/data/', views.CVDataView.as_view(), name='cv_data'),
]


