from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('test/', views.index, name='test'),
]
