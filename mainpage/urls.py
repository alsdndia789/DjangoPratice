from django.urls import path
from .views import *

urlpatterns = [
	path('', overview, name="overview"),
	path('imageupload/', imageUpload, name="imageupload"),
	path('deleteimage/<int:pk>/remove/', deleteimage, name="deleteimage"),
]