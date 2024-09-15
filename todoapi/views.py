# from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from todoapp.models import Todo
from django.utils import timezone
# Authentication
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate  # for login


# Create your views here.
# Auth API
@csrf_exempt
def signup(request):
    if request.method == 'POST':  # Cos GET user Signup data happens on the secondary interface & is being Posted here
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password']) # data replaces request.POST
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'This username has already been taken. Please choose a new username'}, status=400)
        


@csrf_exempt
def login(request):
    if request.method == 'POST': 
        
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password']) # data replaces request.POST
        if user is None:
            return JsonResponse({'error':'Could not login, please check username and password'}, status=400) 
        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)    
            return JsonResponse({'token':str(token)}, status=200)
        
        



# CRUD API
class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated] # To ensure users are authenticated to access TodoCompletedList

    # Ensure users gets todos that are relevant to themselves
    def get_queryset(self):
        user = self.request.user  # Ensures it the current user's todolist that is being accessed
        return Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
    



class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated] 

    # Ensure users gets todos that are relevant to themselves
    def get_queryset(self):
        user = self.request.user  
        return Todo.objects.filter(user=user, datecompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user 
        return Todo.objects.filter(user=user)   




class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user 
        return Todo.objects.filter(user=user)
    
    # Define a method to update todo to completed with the current time of action
    def perform_update(self, serializer):
        serializer.save(datecompleted=timezone.now())

    # def perform_update(self, serializer):
    #     serializer.instance.datecompleted = timezone.now()
    #     serializer.save()




class TodoUnComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_update(self, serializer):
        serializer.save(datecompleted=None)

        



