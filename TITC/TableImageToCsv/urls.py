from django.urls import path
from . import views

app_name = 'TableImageToCsv'

urlpatterns = [
  path('',views.fileUpload,name='index'),
]
