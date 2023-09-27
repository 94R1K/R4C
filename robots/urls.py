from django.urls import path

from robots import views

app_name = 'robots'

urlpatterns = [
    path('download-excel/',
         views.ExcelReportView.as_view(),
         name='download_excel'),
]
