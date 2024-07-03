from django.urls import path
from . import views
from cvback.events.views import BoundingBoxApiView
from graphene_django.views import GraphQLView
from cvback.schema import schema


urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('rest/bounding_box/', BoundingBoxApiView.as_view(), name='mqtt_event'),
]
