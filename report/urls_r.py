from django.urls import path, include
from report import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.ReportDailyRViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
