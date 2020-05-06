
from rest_framework.test import APITestCase
from accounts.models import User
from rest_framework.reverse import reverse
from campaign.models import (CampaignModel as Campaign,
                            CampaignStatusModel,
                            PriceUnitModel)
from rest_framework.reverse import reverse

user_cred = [{"username":"fr1","password":"fr1"},
            {"username":"fr2","password":"fr2"},
            {"username":"mgo1","password":"mgo1"},
            {"username":"donor1","password":"donor1"}
            ]

class MgoAPITestCase(APITestCase):
    def setUp(self):
        u1 = User.objects.create(username="fr1",type="f")
        u1.set_password("fr1")
        u1.save()
        u2 = User.objects.create(username="mgo1",type="m")
        u2.set_password("mgo1")
        u2.save()
        u3 = User.objects.create(username="fr2",type="f")
        u3.set_password("fr2")
        u3.save()
        u4 = User.objects.create(username="donor1",type="d")
        u4.set_password("donor1")
        u4.save()

        p1 = PriceUnitModel.objects.create(unit="CAD")

        c1 = CampaignStatusModel.objects.create(id=0, status="Waiting for approval")
        c2 = CampaignStatusModel.objects.create(id=1, status="Approved")
        c3 = CampaignStatusModel.objects.create(id=2, status="Rejected")

        Campaign.objects.create(title="Test title1",description="Testing1",\
                                    unit_id=p1,amount=3000,created_by_id=u1)
        Campaign.objects.create(title="Test title2",description="Testing2",\
                                    unit_id=p1,amount=3000,inventory=['laptop'],
                                    created_by_id=u2)
        Campaign.objects.create(title="Test title3",description="Testing3",\
                                    unit_id=p1,amount=3000,inventory=['Tablet'],
                                    created_by_id=u1, status_id=c2)

    def authenticate_user(self, data):
        url = reverse('accounts:login')
        response = self.client.post(url, data, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return response

    #Test fails if the user is not authenticated
    def test_user_authentication_fail(self):
        url = reverse('mgo:api-mgo-action')
        resp = self.client.patch(url, format = 'json')
        error = "Authentication credentials were not provided."
        self.assertEqual(resp.data.get("detail", None) , error)
        self.assertNotEqual(resp.status_code, 200)

    #Test passes if the user is authenticated
    def test_user_authentication_success(self):
        url = reverse('mgo:api-mgo-action')
        self.authenticate_user({"username":"mgo1","password":"mgo1"})
        resp = self.client.patch(url, format = 'json')
        error = "Authentication credentials were not provided."
        self.assertNotEqual(resp.data.get("detail", None) , error)

    #Test passes if id and status_type exists in request body
    def test_patch_id_and_status(self):
        url = reverse('mgo:api-mgo-action')
        self.authenticate_user({"username":"mgo1","password":"mgo1"})
        data_list = [{},{"id":3},{"status_type":4}]
        error = {'Error': 'Either id or status not provided'}
        for data in data_list:
            if not data.get("id",None) or not data.get("status_type",None):
                resp = self.client.patch(url, data, format = 'json')
                self.assertEqual(resp.data , error)

    #Input fuzzing test
    def test_patch_id_and_status(self):
        url = reverse('mgo:api-mgo-action')
        self.authenticate_user({"username":"mgo1","password":"mgo1"})
        data_list = [{"id":"asd","status_type":"asd"}]
        for data in data_list:
            resp = self.client.patch(url, data, format = 'json')
            self.assertEqual(resp.status_code , 400)
            self.assertEqual(resp.data, {'Error': 'Check the logs'})

    #Test passes if the user is mgo and request body is valid.
    def test_patch_id_and_status(self):
        url = reverse('mgo:api-mgo-action')
        self.authenticate_user({"username":"mgo1","password":"mgo1"})
        first_id = Campaign.objects.first().id
        data_list = [{"id":first_id,"status_type":"Rejected"}]
        for data in data_list:
            resp = self.client.patch(url, data, format = 'json')
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(resp.data, {'Success': 'Campaign updated'})

    #Test fails if the user is not mgo. Permission denied.
    def test_patch_id_and_status(self):
        url = reverse('mgo:api-mgo-action')
        self.authenticate_user({"username":"fr1","password":"fr1"})
        first_id = Campaign.objects.first().id
        data_list = [{"id":first_id,"status_type":"Approved"}]
        for data in data_list:
            resp = self.client.patch(url, data, format = 'json')
            self.assertEqual(resp.status_code , 401)
            self.assertEqual(resp.data, {'Error': 'Permission Denied'})
