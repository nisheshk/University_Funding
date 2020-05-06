from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework.reverse import reverse

class UserAPITestCase(APITestCase):

    #Creates an instance and saves it in test database
    def setUp(self):
        user = User.objects.create(username="nis@uwindsor.ca")
        user.set_password("nis@uwindsor.ca")
        user.save()

    #Test if the user is created by old standard approach
    def test_created_user_standard_way(self):
        qs = User.objects.filter(username="nis@uwindsor.ca")
        self.assertEqual(qs.count(), 1)

    #Test created user by making the use of API endpoint
    #self.client is an APIClient instance. APIClient inherits from
    #django standard Client class. Hence all the standard get(), post(), put(),
    #  .patch(), .delete(), .head() and .options() methods are all available.
    def test_created_user_api(self):
        url = reverse('accounts:login')    #reverse(namespace:name)
        data = {
        "username":"nis@uwindsor.ca",
        "password":"nis@uwindsor.ca"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)


    #Test fails when username provided is Incorrect
    def test_created_user_api_username_fail(self):
        url = reverse('accounts:login')
        data = {
        "username":"nis@uwindsor.caa",
        "password":"nis@uwindsor.ca"
        }
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.data, {'Error': 'Incorrect email address'})

    #Test fails when username password is Incorrect
    def test_created_user_api_password_fail(self):
        url = reverse('accounts:login')
        data = {
        "username":"nis@uwindsor.ca",
        "password":"nis@uwindsor.caa"
        }
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.data, {'Error': 'Incorrect Password'})

    #Test passes if the token is created after the user login
    def test_login_token_created(self):
        url = reverse('accounts:login')
        data = {
        "username":"nis@uwindsor.ca",
        "password":"nis@uwindsor.ca"
        }
        response = self.client.post(url, data, format='json')
        #print (dir(response))
        resp = response.data
        token = resp.get('access', 0)
        token_length = 0
        if token != 0:
            token_length = len(token)

        self.assertGreater(token_length, 0)

    #Test passes if the session variables are set correctly.
    def test_session_variables(self):
        url = reverse('accounts:login')
        data = {
        "username":"nis@uwindsor.ca",
        "password":"nis@uwindsor.ca"
        }
        self.assertEqual(self.client.session.get('username',None), None)
        response = self.client.post(url, data, format='json')
        #print (dir(response))
        session = self.client.session
        self.assertEqual(session.get('username'),data['username'])
        self.assertEqual(session.get('access_token'),response.data.get('access'))
        self.assertEqual(session.get('user_type'),response.data.get('user_type'))

    #Test passes if the token is created after the user login
    def test_login_token_not_created(self):
        url = reverse('accounts:login')
        data = {
        "username":"nis@uwindsor.caa",
        "password":"nis@uwindsor.ca"
        }
        response = self.client.post(url, data, format='json')
        #print (dir(response))
        resp = response.data
        token = resp.get('access', 0)
        token_length = 0
        if token != 0:
            token_length = len(token)

        self.assertEqual(token_length, 0)

    #This test case fails for now. Need to change the code later
    #Authenticated users should not be able to login again.
    def test_authenticated_user_login_again(self):
        url = reverse('accounts:login')
        data = {
        "username":"nis@uwindsor.ca",
        "password":"nis@uwindsor.ca"
        }
        response = self.client.post(url, data, format='json')
        token = response.data.get('access', 0)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, 403)

    #Test fails if the non-authenticated user tries to logout.
    def test_user_logout_fail(self):
        logout_url = reverse('accounts:logout')
        response = self.client.get(logout_url, format='json')
        self.assertNotEqual(response.status_code, 200)

    #Test passes if the authenticated user tries to logout.
    def test_user_logout_pass(self):
        logout_url = reverse('accounts:logout')
        login_url = reverse('accounts:login')
        data = {
        "username":"nis@uwindsor.ca",
        "password":"nis@uwindsor.ca"
        }

        #User logs in with correct credentials
        resp = self.client.post(login_url, data, format='json')
        token = resp.data.get('access')

        #In the next request fot that user , token is passed in the headers
        #If token exists in the header and the session has not expired,
        #then it means the user is logged in.
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        logged_in_session = self.client.session
        self.assertEqual(logged_in_session.get('username',None),data['username'])

        #The user should be able to logout since the user is logged in.
        response = self.client.get(logout_url, format='json')
        logged_out_session = self.client.session
        self.assertEqual(response.status_code, 200)

        #After the user is logged out, the session variables must be killed.
        self.assertNotEqual(logged_out_session.get('username',None),\
                            data['username'])
