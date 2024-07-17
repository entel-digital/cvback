import graphene
from graphene_django.filter import DjangoFilterConnectionField
from cvback.events.schema import (LabelType, KeyFrameType, BoundingBoxType, EventTypeType, EventType)
from cvback.events.models import (Label, KeyFrame, BoundingBox, Event)

class UpdateEventMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        tag = graphene.String()

    event = graphene.Field(EventType)

    def mutate(self, info, id, tag):
        event = Event.objects.get(pk=id)
        event.tag = tag
        event.save()
        return UpdateEventMutation(event=event)

class Query(graphene.ObjectType):
    all_events = graphene.List(EventType)
    #event_type = graphene.Field(EventTypeType)
    #all_labels = graphene.List(LabelType)
    #all_bounding_boxes = graphene.List(BoundingBoxType)
    #all_key_frames = graphene.List(KeyFrameType)
    def resolve_all_events(self, info):
        return Event.objects.all()
    
    paginated_events = DjangoFilterConnectionField(
        EventType,
        first=graphene.Int(),
        skip=graphene.Int()
    )
    def resolve_paginated_events(self, info, **kwargs):
        qs = Event.objects.all()
        skip = kwargs.get('skip')
        first = kwargs.get('first')
        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
        return qs

class Mutation(graphene.ObjectType):
    update_event = UpdateEventMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
