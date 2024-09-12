from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import response
from django.http import JsonResponse


@api_view(['GET'])
def demo(request):
    return JsonResponse({'hello':'hi'})

