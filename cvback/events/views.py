from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import AreaOfInterest
from .serializers import AreaOfInterestSerializer


# Create your views here.
# TODO: filter by camera
@csrf_exempt
def areas_of_interest_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        areas_of_interest = AreaOfInterest.objects.all()
        serializer = AreaOfInterestSerializer(areas_of_interest, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AreaOfInterestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def area_of_interest_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        area_of_interest = AreaOfInterest.objects.get(pk=pk)
    except AreaOfInterest.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AreaOfInterestSerializer(area_of_interest)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AreaOfInterestSerializer(area_of_interest, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        area_of_interest.delete()
        return HttpResponse(status=204)
