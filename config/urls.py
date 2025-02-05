from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/report_daily_d/', include('report_daily.urls_d')),
    path('api/v1/report_daily_r/', include('report_daily.urls_r')),
    path('api/v1/category/', include('category.urls')),
]
