# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'app_employies'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.HomeView.as_view(), name='home'),
    path('details/<uuid:pk>', views.Details.as_view(), name='details'),
    path('details/edit/<uuid:pk>', views.EditEmpView.as_view(), name='edit_emp'),
    path('add/', views.add, name='add'),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
