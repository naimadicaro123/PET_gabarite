# core/urls.py
from django.urls import path
from .views import UploadProvaAPIView

urlpatterns = [
    path('upload-prova/', UploadProvaAPIView.as_view(), name='upload_prova_api'),
]