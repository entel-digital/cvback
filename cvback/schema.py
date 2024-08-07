import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.utils import camelize
from graphene_django_optimizer import query, OptimizedDjangoObjectType, resolver_hints
from cvback.events.models import Event, EventType, Label
from django.db.models import Count
import json
from asyncio import iscoroutinefunction
from cvback.events.schema import FrameType

def optional_query(func):
    if iscoroutinefunction(func):
        return query(func)
    return func

class OptimizedEventType(OptimizedDjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"
        filter_fields = {
            'id': ['exact', 'range', 'in', 'gte', 'lt'],
            'informed_date': ['gte', 'lt', 'exact']
        }
        interfaces = (graphene.relay.Node,)

    id = graphene.ID(source='pk', required=True)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related(
            'event_type', 
            'event_label'
        ).prefetch_related(
            'frames', 
            'labels_detected', 
            'labels_missing',
            'inference_detection_classification',
            'inference_ocr',
            'inference_detection_classification__labels',
            'inference_detection_classification__bounding_boxes',
        )

    @resolver_hints(
        model_field='frames',
        prefetch_related='frames',
    )
    def resolve_frames(self, info):
        return self.frames.all()
    
    def resolve_id(self, info):
        return self.pk    

class UpdateEventMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        tag = graphene.String()

    event = graphene.Field(OptimizedEventType)

    def mutate(self, info, id, tag):
        event = Event.objects.get(pk=id)
        event.tag = tag
        event.save()
        return UpdateEventMutation(event=event)

class EventFilterAndPaginationType(graphene.ObjectType):
    events = graphene.List(OptimizedEventType)
    global_total_number = graphene.Int()
    offset = graphene.Int(default_value=0)
    rows_per_page = graphene.Int(default_value=10)
    filtered = graphene.Boolean()
    filtered_by = graphene.List(graphene.String)
    label_text_filter = graphene.String()
    query_total_number = graphene.Int()
    labels_summary = graphene.JSONString()
    types_summary = graphene.JSONString()
    unique_labels_count = graphene.Int()

class Query(graphene.ObjectType):
    all_events = graphene.List(OptimizedEventType)

    @optional_query
    def resolve_all_events(self, info):
        return OptimizedEventType.get_queryset(Event.objects.all(), info)

    paginated_events = DjangoFilterConnectionField(
        OptimizedEventType,
        first=graphene.Int(),
        skip=graphene.Int()
    )

    @optional_query
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
        id_greater_than_equal=graphene.Int(default_value=None),
        date_equals_to=graphene.DateTime(default_value=None),
        date_lower_than=graphene.DateTime(default_value=None),
        date_greater_than_equal=graphene.DateTime(default_value=None),
        label_text_filter=graphene.String(),
    )

    @optional_query
    def resolve_filtered_and_paginated_events(self, info, **kwargs):
        qs = Event.objects.order_by('-informed_date')
        global_total_number = qs.count()

        rows_per_page = kwargs.get('rows_per_page', 10)
        offset = kwargs.get('offset')
        id_equals_to = kwargs.get('id_equals_to')
        id_lower_than = kwargs.get('id_lower_than')
        id_greater_than_equal = kwargs.get('id_greater_than_equal')
        date_equals_to = kwargs.get('date_equals_to')
        date_lower_than = kwargs.get('date_lower_than')
        date_greater_than_equal = kwargs.get('date_greater_than_equal')
        label_text_filter = kwargs.get('label_text_filter')

        filtered = False
        filtered_by = []

        if label_text_filter:
            filtered = True
            filtered_by.append("label_text")
            qs = qs.filter(event_label__name__icontains=label_text_filter)
        if id_equals_to:
            filtered = True
            filtered_by.append("id=")
            qs = qs.filter(id=id_equals_to)
        if id_lower_than:
            filtered = True
            filtered_by.append("id<")
            qs = qs.filter(id__lt=id_lower_than)
        if id_greater_than_equal:
            filtered = True
            filtered_by.append("id>=")
            qs = qs.filter(id__gte=id_greater_than_equal)
        if date_equals_to:
            filtered = True
            filtered_by.append("date=")
            qs = qs.filter(informed_date=date_equals_to)
        if date_lower_than:
            filtered = True
            filtered_by.append("date<")
            qs = qs.filter(informed_date__lt=date_lower_than)
        if date_greater_than_equal:
            filtered = True
            filtered_by.append("date>=")
            qs = qs.filter(informed_date__gte=date_greater_than_equal)

        qs = OptimizedEventType.get_queryset(qs, info)
                
        total = qs.count()

        # Calculate summaries
        all_labels = Label.objects.all()
        labels_summary = {label.name: count for label in all_labels if (count := qs.filter(event_label=label).count()) > 0}
        labels_summary['total'] = total

        all_types = EventType.objects.all()
        types_summary = {event_type.name: count for event_type in all_types if (count := qs.filter(event_type=event_type).count()) > 0}
        types_summary['total'] = total

        unique_labels_count = sum(1 for count in labels_summary.values() if count > 0) - 1

        if offset:
            qs = qs[offset:]
        if rows_per_page:
            qs = qs[:rows_per_page]

        result = EventFilterAndPaginationType(
            events=qs,
            global_total_number=global_total_number,
            offset=offset,
            rows_per_page=rows_per_page,
            filtered=filtered,
            filtered_by=filtered_by,
            query_total_number=total,
            labels_summary=json.dumps(labels_summary),
            types_summary=json.dumps(types_summary),
            unique_labels_count=unique_labels_count
        )

        return result

class Mutation(graphene.ObjectType):
    update_event = UpdateEventMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)