from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import User, UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class Register(APIView):
    def post(self, request):
        print(request.data)
        email, password = request.data['email'], request.data['password']
        try:
            user = User.objects.create_user(email, password)
            UserProfile.objects.create(user=user)
        except Exception as e:
            return Response({'details': f'error: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        

        return Response({'details': 'user created'}, status=status.HTTP_201_CREATED)


class ProfileContent(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = 


        

            
            
