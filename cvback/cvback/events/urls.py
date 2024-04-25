from django.urls import path
from . import views
from graphene_django.views import GraphQLView
from cvback.schema import schema

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]

