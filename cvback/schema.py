import graphene
from graphene_django.filter import DjangoFilterConnectionField
from cvback.events.schema import EventType, EventFilterAndPaginationType, EventPropertySummaryType
from cvback.events.models import Event, Label, EventType as EventTypeModel
import json


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
    # event_type = graphene.Field(EventTypeType)
    # all_labels = graphene.List(LabelType)
    # all_bounding_boxes = graphene.List(BoundingBoxType)
    # all_key_frames = graphene.List(KeyFrameType)

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

    filtered_and_paginated_events = graphene.Field(
        EventFilterAndPaginationType,
        offset=graphene.Int(default_value=0),
        rows_per_page=graphene.Int(default_value=10),
        id_equals_to=graphene.Int(default_value=None),
        id_lower_than=graphene.Int(default_value=None),
        id_greather_than_equal=graphene.Int(default_value=None),
        date_equals_to=graphene.Date(default_value=None),
        date_lower_than=graphene.Date(default_value=None),
        date_greather_than_equal=graphene.Date(default_value=None),
        label_text_filter=graphene.String()
        )

    def resolve_filtered_and_paginated_events(self, info, **kwargs):
        qs = Event.objects.order_by('-informed_date')
        total_number = len(qs)

        rows_per_page = kwargs.get('rows_per_page', 10)
        offset = kwargs.get('offset')
        id_equals_to = kwargs.get('id_equals_to')
        id_lower_than = kwargs.get('id_lower_than')
        id_greater_than_equal = kwargs.get('id_greater_than_equal')
        date_equals_to = kwargs.get('date_equals_to')
        date_lower_than = kwargs.get('date_lower_than')
        date_greater_than_equal = kwargs.get('date_greater_than_equal')
        date_greater_than_equal = kwargs.get('filter')
        label_text_filter = kwargs.get('label_text_filter')

        filtered = False
        filtered_by = []
        if label_text_filter:
            filtered = True
            filtered_by.append("label_text")
            qs.filter(event_label__name__icontains=label_text_filter)
        if id_equals_to:
            filtered = True
            filtered_by.append("id=")
            qs.filter(id=id_equals_to)
        if id_lower_than:
            filtered = True
            filtered_by.append("id<")
            qs.filter(id__lt=id_lower_than)
        if id_greater_than_equal:
            filtered = True
            filtered_by.append("id>=")
            qs.filter(id__gte=id_greater_than_equal)

        if date_equals_to:
            filtered = True
            filtered_by.append("date=")
            qs.filter(date=date_equals_to)
        if date_lower_than:
            filtered = True
            filtered_by.append("date<")
            qs.filter(date__lt=date_lower_than)
        if date_greater_than_equal:
            filtered = True
            filtered_by.append("date>=")
            qs.filter(date__gte=date_greater_than_equal)

        if offset:
            qs = qs[offset:]
        if rows_per_page:
            qs = qs[:rows_per_page]

        result = EventFilterAndPaginationType(
            events=qs,
            total_number=total_number,
            offset=offset,
            rows_per_page=rows_per_page,
            filtered=filtered,
            filtered_by=filtered_by
        )

        return result

    event_types_summary = graphene.Field(
        EventPropertySummaryType
    )

    def resolve_event_types_summary(self, info, **kwargs):
        event_types = EventTypeModel.objects.all()
        total = Event.objects.count()
        summary = {"total": total}

        for event_type in event_types:
            event_type_number = Event.objects.filter(event_type=event_type).count()
            if event_type_number>0:
                summary[event_type.name] = event_type_number 
        summary = json.dumps(summary)
        return EventPropertySummaryType(
            summary=summary
        )

    event_labels_summary = graphene.Field(
        EventPropertySummaryType
    )

    def resolve_event_labels_summary(self, info, **kwargs):
        
        event_labels = Event.event_label.get_queryset().distinct()

        total = Event.objects.count()
        summary = {"total": total}

        for event_label in event_labels:
            summary[event_label.name] = Event.objects.filter(event_label=event_label).count()
        summary = json.dumps(summary)
        return EventPropertySummaryType(
            summary=summary
        )

class Mutation(graphene.ObjectType):
    update_event = UpdateEventMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

"""{eventLabelsSummary {summary}}"""
