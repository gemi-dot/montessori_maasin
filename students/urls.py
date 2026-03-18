from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('barcode-input/', views.barcode_input, name='barcode_input'),
    # path('scanner/', views.scanner, name='scanner'),
]