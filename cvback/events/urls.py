from django.urls import path
from . import views

urlpatterns = [
    path('rest/aoi/', views.areas_of_interest_list),
    path('rest/aoi/<int:pk>/', views.area_of_interest_detail),
]
