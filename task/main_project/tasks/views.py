from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
from rest_framework import status
from rest_framework import generics
#from snippets.models import Snippet



@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : 'task-list/',
        'Detail View' : 'task-detail/<str:pk>/',
        'Create' : 'task-create/',
        'Update' : 'task-update/<str:pk>/',
        'Delete' : 'task-delete/<str:pk>/',
    

    }
    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many = True)
    return Response(serializer.data)
@api_view(['GET'])
def taskDetail(request, pk):
    try:
        tasks = Task.objects.get(id=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many = False)
    return Response(serializer.data)
@api_view(['POST'])
def taskCreate(request):
    data=request.data
    if isinstance(request.data, list):
        return bulkadd(data)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        object=serializer.data["id"]
        return Response("id:{}".format(object),status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def bulkadd(data):

        tasks = request.data.pop(tasks)
        models = []
        for tasks in tasks:
            # validate each model with one seat at a time
            request.data['tasks'] = tasks
            serializer =TaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            models.append(serializer)

        saved_models = [model.save() for model in models]
        result_serializer =TaskSerializer(saved_models, many=True)
        return Response(result_serializer.data)
@api_view(['PUT'])
def taskUpdate(request, pk):
    task = Task.objects.get(id = pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def taskDelete(request, pk):
    try:
        task = Task.objects.get(pk = pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
