from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.solicitacao_confirmacao_upload, name="upload"),
    ]
