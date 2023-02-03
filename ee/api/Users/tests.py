from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
import json
from .models import User


class MyProfileTestCase(APITestCase):
    def register(self):
        response = self.client.post('/api/user/register/', {'email':'khaled2@gmail.com', 'password': 'django.124343'}, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        from api.Users.models import User
        user = User.objects.get(email='khaled2@gmail.com')
        self.assertEqual('khaled2@gmail.com', user.email)
    
    def make_profile(self):
        body = {
            'email':'khaled2@gmail.com',
            'date_of_birth': '2000-1-1',
            'phone': '10094238',
            'code_country': '+20' }
        response = self.client.post('/api/user/profile/create/',body , format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_token(self):
        response = self.client.post('/api/api-token-auth/', {'username': 'khaled2@gmail.com', 'password':'django.124343'})
        response_load = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response_load['token']

    def get_my_profile(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/user/profile/my/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.content, response.status_code
    
    def is_profile_found(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/user/profile/my/', format='json')
        return response.status_code != status.HTTP_404_NOT_FOUND


    def test_register(self):
       self.register()

    def test_make_profile(self):
        self.register()
        self.make_profile()

    def test_get_token(self):
        self.register()
        self.make_profile()
        self.get_token
       
    def test_get_my_profile(self):
        self.register()
        self.make_profile()
        token = self.get_token()
        self.get_my_profile(token)


    def test_update_my_profile(self):
        self.register()
        self.make_profile()
        token = self.get_token()

        body = {
            'date_of_birth': '2000-1-2',
            'phone': '10094238',
            'code_country': '+20' }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.put('/api/user/profile/my/', body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = json.loads(self.get_my_profile(token)[0])
        self.assertEqual(profile['date_of_birth'], '2000-01-02')

    def test_delete_my_profile(self):
        self.register()
        self.make_profile()
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/api/user/profile/my/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.is_profile_found(token))
        

       

        
class TestCountryCodes(APITestCase):
    def test_get_country_codes(self):
        response = self.client.get('/api/user/country_code/')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        


class ProfileTestCase(APITestCase):
    def register(self, email, password):
        response = self.client.post('/api/user/register/', {'email': email, 'password': password}, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        from api.Users.models import User
        user = User.objects.get(email=email)
        self.assertEqual(email, user.email)
        return user

    def get_token(self, username, password):
        response = self.client.post('/api/api-token-auth/', {'username': username, 'password':password})
        response_load = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response_load['token']

    def make_profile(self, email, dob, phone, code_country):
        body = {
            'email':email,
            'date_of_birth': dob,
            'phone': phone,
            'code_country': code_country }
        response = self.client.post('/api/user/profile/create/',body , format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def get_profile(self, token, id_profile):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(f'/api/user/profile/{id_profile}/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.content, response.status_code


    def test_get_profile(self):
        self.register('khaled@gmail.com', 'django.123')
        cur_user_token = self.get_token('khaled@gmail.com', 'django.123')
        user = self.register('Ahmed@gmail.com', 'django.123')
        self.make_profile(user.email, '2000-1-1', '1348913', '+20')
        content, status_code = self.get_profile(cur_user_token, user.id)
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_delete_profile(self):
        self.register('khaled@gmail.com', 'django.123')
        cur_user_token = self.get_token('khaled@gmail.com', 'django.123')
        user = self.register('Ahmed@gmail.com', 'django.123')
        self.make_profile(user.email, '2000-1-1', '1348913', '+20')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + cur_user_token)
        response = self.client.delete(f'/api/user/profile/{user.id}/')
        self.assertEqual(response.status_code, 403)
        print(response.content)

    def test_delete_my_profile(self):
        
        user = self.register('Ahmed@gmail.com', 'django.123')
        cur_user_token = self.get_token('Ahmed@gmail.com', 'django.123' )
        self.make_profile(user.email, '2000-1-1', '1348913', '+20')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + cur_user_token)
        response = self.client.delete(f'/api/user/profile/{user.id}/')
        self.assertEqual(response.status_code, 204)
        
    def test_update_profile(self):
        self.register('khaled@gmail.com', 'django.123')
        cur_user_token = self.get_token('khaled@gmail.com', 'django.123')
        user = self.register('Ahmed@gmail.com', 'django.123')
        self.make_profile(user.email, '2000-1-1', '1348913', '+20')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + cur_user_token)
        body = {
            'date_of_birth': '2000-1-2',
            'phone': '13483313',
            'code_country': '+20' 
        }
        response = self.client.put(f'/api/user/profile/{user.id}/', json=body)
        self.assertEqual(response.status_code, 403)


    def test_update_my_profile(self):
        user = self.register('Ahmed@gmail.com', 'django.123')
        cur_user_token = self.get_token('Ahmed@gmail.com', 'django.123' )
        self.make_profile(user.email, '2000-1-1', '1348913', '+20')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + cur_user_token)
        body = {
            'date_of_birth': '2000-01-02',
            'phone': '13483313',
            'code_country': '+20' 
        }
        response = self.client.put(f'/api/user/profile/{user.id}/', body, format='json')
        self.assertEqual(response.status_code, 200)
        profile_after_update, status_code = self.get_profile(cur_user_token, user.id)
        profile_after_update  = json.loads(profile_after_update)
        for key in body:
            self.assertEqual(body[key], profile_after_update[key])

       
        
        

