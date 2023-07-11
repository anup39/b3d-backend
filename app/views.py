from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .tasks import handleExampleTask
# Create your views here.


class ExampleViewSet(viewsets.ViewSet):
    def list(self, request):
        # Your logic for processing the API request
        data = {
            'message': 'Hello, API!',
            'status': 'success'
        }
        handleExampleTask.delay()

        return Response(data)