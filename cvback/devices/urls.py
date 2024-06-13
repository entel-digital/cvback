from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cvback.devices.views import AreaViewSet, CameraViewSet, InferenceComputerViewSet
from . import views


router = DefaultRouter()
router.register(r'areas', AreaViewSet)
router.register(r'cameras', CameraViewSet)
router.register(r'nference_computers', InferenceComputerViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path('', include(router.urls))
    ]
