from django.urls import path
from .views import *

urlpatterns = [
    path('', overview, name="overview"),
    path('imageupload/', image_upload, name="imageupload"),
    path('imagedelete/<int:pk>/remove/', image_delete, name="imagedelete"),
    path('imagedetail/<int:pk>/', image_detail, name="imagedetail"),
    path('todolist/', todo_list_page, name="todolist"),
]
