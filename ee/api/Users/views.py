from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import User, UserProfile, ImageUpload
from .serializers import UserProfileSerializer, ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework import mixins
import json
from api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny

# Create your views here.

# ============ helper functions ========== #
def get_country_codes() -> list:
    from .CountryCodes import country_codes
    return country_codes

# ============= it is helper class used to deal with tokens ============= #
class TokenOperations:
    @staticmethod
    def get_token_object(token:str):
        return get_object_or_404(Token, key=token)

    @staticmethod
    def get_token_value(request)->str:
        # 'Token 18iwejwjr9o1j'.splitez()[1]
        try:
            return request.META.get('HTTP_AUTHORIZATION').split(' ')[1] 
        except:
            return None # if not auth
    
    @staticmethod
    def get_user_from_request_token(request):
        token_value = TokenOperations.get_token_value(request)
        token = TokenOperations.get_token_object(token=token_value)
        if token is None:
            return None
        return token.user


class Register(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        print(request.data)
        email, password = request.data['email'], request.data['password']
        try:
            user = User.objects.create_user(email, password)
            # UserProfile.objects.create(user=user)
        except Exception as e:
            return Response({'details': f'error: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        
  
        return Response({'details': 'user created'}, status=status.HTTP_201_CREATED)



class ImageUploadObject(APIView):
    # ---------------- helper methods ------------------- #
    def get_profile(self, request):
        user = TokenOperations.get_user_from_request_token(request)
        if user is None:
            return
        return user.profile_name

    def assign_image_to_profile(self, request, Image):
        profile = self.get_profile(request)
        profile.picture = Image
        profile.save()
    def get_image_of_auth(self, request):
        profile = self.get_profile(request)
        if profile is None:
            return None
        return profile.picture

    # ------------------ main methods -------------------- #
    def put(self, request):
        try:
            file = request.data['file']
        except KeyError:
            return Response({'details': 'Request has no resource file attached'}, status=status.HTTP_400_BAD_REQUEST)
        Image = ImageUpload.objects.create(image=file)
        self.assign_image_to_profile(request, Image)
        return Response({'details': 'uploaded successfully', 'Image_id': Image.id}, status=status.HTTP_201_CREATED)

    
    def get(self, request):
        image = self.get_image_of_auth(request)
        if image is None:
            return Response({'details': 'image not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ImageUploadSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

    


class UserProfileCreation(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
        try:
            user.profile_name
            return Response({'details': 'user already have profile'}, status=status.HTTP_403_FORBIDDEN)
        except:
            pass
        date_of_birth = request.data['date_of_birth']
        phone = request.data['phone']
        code_country = request.data['code_country']
        try:
            UserProfile.objects.create(user=user,
                                        date_of_birth=date_of_birth,
                                        phone=phone, code_country= code_country,
            )
        except Exception as e:
            return Response({'details': f'create is failed, {e}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'details': 'created sucessfully'}, status=status.HTTP_201_CREATED)


class UserProfileObject(APIView):
    # ---------------- helper methods ------------------- #
    def get_profile_object(self, request):
        user = TokenOperations.get_user_from_request_token(request)
        try:
            return user.profile_name
        except:
            return None
         
    # ----------------- main methods ---------------------  #
    def get(self, request):
        profile = self.get_profile_object(request)
        if profile is None:
            return Response({'details': 'the profile is not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        profile = self.get_profile_object(request)
        if profile is None:
            return Response({'details': 'the profile is not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'details', 'the update is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'details', 'profile updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request):
        profile = self.get_profile_object(request)
        if profile is None:
            return Response({'details': 'the profile is not found'}, status=status.HTTP_404_NOT_FOUND)
        profile.delete()
        return Response({'details', 'profile deleted successfully'}, status=status.HTTP_200_OK)


class UserProfileObject2(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'user_id'

    def get(self, request, user_id):
        return self.retrieve(request)
    
    def put(self, request, user_id):
        return self.update(request)
    
    def delete(self, request, user_id):
        return self.destroy(request)

class CountryCodes(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        return Response({'country_codes': get_country_codes()})
        

