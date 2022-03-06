from django.urls import path
from .views import *

urlpatterns = [
    path('', overview, name="overview"),
    path('imageupload/', imageUpload, name="imageupload"),
    path('imagedelete/<int:pk>/remove/', imagedelete, name="imagedelete"),
    path('imagedetail/<int:pk>/', imagedetail, name="imagedetail"),
]
