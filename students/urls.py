from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('barcode-input/', views.barcode_input, name='barcode_input'),
    path('scan-student-id/', views.scan_student_id, name='scan_student_id'),
    path('scan-qr-code/', views.scan_qr_code, name='scan_qr_code'),
    #path('scanner/', views.scanner, name='scanner'),

    #path('scanner/', views.student_list, name='scanner_page'),

    path('scanner/', views.scanner_page, name='scanner_page'),
    path('get-student/<str:barcode_id>/', views.get_student),

    path('scan/<str:barcode_id>/', views.submit_scan, name='submit_scan'),
]