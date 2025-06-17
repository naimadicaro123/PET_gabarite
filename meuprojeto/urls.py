from django.contrib import admin
from django.urls import path, include

# urls.py
from rest_framework.routers import DefaultRouter
from leitorapp.views import UploadViewSet, ParticipanteViewSet, ProvaViewSet, ResultadoViewSet
from rest_framework import routers

route = DefaultRouter()
route.register(r'ler-imagem', UploadViewSet, basename='ler-imagem')
route.register(r'participantes', ParticipanteViewSet, basename='participantes')
route.register(r'provas', ProvaViewSet, basename='provas-gabaritos')
route.register(r'resultados', ResultadoViewSet, basename="resultados")

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include(route.urls))
]
