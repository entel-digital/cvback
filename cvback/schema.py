import graphene
from graphene_django.filter import DjangoFilterConnectionField
import graphene_django_optimizer as gql_optimizer
from cvback.events.models import Event, EventType, Label, InferenceDetectionClassification
import json
from asyncio import iscoroutinefunction
from cvback.events.schema import FrameType
from django.db.models import Prefetch
from datetime import datetime, timedelta

def optional_query(func):
    if iscoroutinefunction(func):
        return gql_optimizer.query(func)
    return func

class OptimizedEventType(gql_optimizer.OptimizedDjangoObjectType):
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
        return gql_optimizer.query(queryset.select_related(
            'event_type', 
            'event_label'
        ).prefetch_related(
            'frames', 
            'videos',
            'key_frames',
            'key_videos',
            'labels_detected', 
            'labels_missing',
            'inference_ocr',
            Prefetch('inference_detection_classification', 
                    queryset=InferenceDetectionClassification.objects.select_related('frame')
                                                                    .prefetch_related('labels', 'bounding_boxes'))
        ), info)

    @gql_optimizer.resolver_hints(
        model_field='frames',
    )
    def resolve_frames(self, info):
        return self.frames.all()
    
    def resolve_id(self, info):
        return self.pk

class UpdateEventMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        tag = graphene.String()

    class Meta:
        output = OptimizedEventType

    @classmethod
    def mutate(cls, root, info, id, tag):
        event = Event.objects.get(pk=id)
        event.tag = tag
        event.save()
        return gql_optimizer.query(Event.objects.filter(pk=event.pk), info).first()

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
    query_total_events_year=graphene.Int()
    query_total_events_month=graphene.Int()
    query_total_events_day=graphene.Int()
    query_total_events_week=graphene.Int()

class Query(graphene.ObjectType):
    all_events = graphene.List(OptimizedEventType)

    @optional_query
    def resolve_all_events(self, info):
        return Event.objects.all()

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
        id_equals_to=graphene.String(default_value=None),
        id_lower_than=graphene.String(default_value=None),
        id_greater_than_equal=graphene.String(default_value=None),
        date_equals_to=graphene.DateTime(default_value=None),
        date_lower_than=graphene.DateTime(default_value=None),
        date_greater_than_equal=graphene.DateTime(default_value=None),
        label_text_filter=graphene.String(),
    )

    @optional_query
    def resolve_filtered_and_paginated_events(self, info, **kwargs):
        qs = Event.objects.order_by('-informed_date')
        global_total_number = Event.objects.count()

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

        now = datetime.now()
        this_year_first_day = datetime(now.year,1,1,0,0,0).astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
        qs2 = qs.filter(informed_date__gte=this_year_first_day)
        this_year_event_number = len(qs2)
        this_month_first_day = datetime(now.year,now.month,1,0,0,0).astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
        qs2 = qs2.filter(informed_date__gte=this_month_first_day)
        this_month_event_number = len(qs2)
        this_week_first_day = now-timedelta(days=now.weekday())
        this_week_first_day = datetime(this_week_first_day.year, this_week_first_day.month,this_week_first_day.day,0,0,0).astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
        qs2 = qs2.filter(informed_date__gte=this_week_first_day)
        this_week_event_number = len(qs2)
        this_day_start = datetime(now.year,now.month,now.day,0,0,0).astimezone().strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
        qs2 = qs2.filter(informed_date__gte=this_day_start)
        this_day_event_number = len(qs2)
        print(this_year_event_number, this_year_first_day)
        print(this_month_event_number,this_month_first_day)
        print(this_day_event_number,this_day_start)
        print(this_week_event_number,this_week_first_day)


        if offset:
            qs = qs[offset:]
        if rows_per_page:
            qs = qs[:rows_per_page]        

        result = EventFilterAndPaginationType(
            events=gql_optimizer.query(qs, info),
            global_total_number=global_total_number,
            offset=offset,
            rows_per_page=rows_per_page,
            filtered=filtered,
            filtered_by=filtered_by,
            query_total_number=total,
            labels_summary=json.dumps(labels_summary),
            types_summary=json.dumps(types_summary),
            unique_labels_count=unique_labels_count,
            query_total_events_year=this_year_event_number,
            query_total_events_month=this_month_event_number,
            query_total_events_day=this_day_event_number,
            query_total_events_week=this_week_event_number
        )

        return result

    
class Mutation(graphene.ObjectType):
    update_event = UpdateEventMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)