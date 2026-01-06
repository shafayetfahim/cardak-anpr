from django.urls import path
from . import views

urlpatterns = [
    # This maps 'http://localhost:8000/indexer/upload/'
    path('upload/', views.upload_vehicle, name='upload'),
]