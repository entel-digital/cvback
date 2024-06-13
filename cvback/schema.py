import graphene
from cvback.events.schema import AreaOfInterestType, BoundingBoxType, InferenceType, EventType
from cvback.events.models import *

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
    all_areas_of_interest = graphene.List(AreaOfInterestType)
    all_bounding_boxes = graphene.List(BoundingBoxType)
    all_inferences = graphene.List(InferenceType)
    all_events = graphene.List(EventType)

    def resolve_all_areas_of_interest(self, info):
        return AreaOfInterest.objects.all()

    def resolve_all_bounding_boxes(self, info):
        return BoundingBox.objects.all()
    
    def resolve_all_inferences(self, info):
        return Inference.objects.all()
    
    def resolve_all_events(self, info):
        return Event.objects.all()

class Mutation(graphene.ObjectType):
    update_event = UpdateEventMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
