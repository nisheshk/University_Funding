
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

class CamapaignAPITestCase(APITestCase):
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


    def campaign_db_query(self, filter_cond):
        obj = Campaign.objects.filter(**filter_cond)
        return obj

    def test_active_campaign(self):
        url = reverse('campaign:api-campaign-active')
        resp = self.client.post(url, format = 'json')
        data = self.campaign_db_query({"status_id":1})
        self.assertEqual(len(resp.data), len(data))
        self.assertEqual(resp.status_code, 200)

    def authenticate_user(self, data):
        url = reverse('accounts:login')
        response = self.client.post(url, data, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return response



    #Test passes if the user is authenticated
    def test_on_waiting_campaigns(self):
        url = reverse('campaign:api-campaign-awaiting')
        resp = self.client.post(url, format = 'json')
        error = "Authentication credentials were not provided."
        self.assertEqual(resp.data["detail"] , error)
        self.assertNotEqual(resp.status_code, 200)

    #Test passes if user has authentication and permission
    def test_on_waiting_campaigns_permission(self):
        for each_user_cred in user_cred:
            login_resp = self.authenticate_user(each_user_cred)
            url = reverse('campaign:api-campaign-awaiting')
            resp = self.client.post(url, format = 'json')
            try:
                error = "Authentication credentials were not provided."
                self.assertNotEqual(resp.data["detail"] , error)
            except:
                pass

            session = self.client.session
            user_type = session.get('user_type')
            data = {"status_id":0}
            if user_type == "d":
                self.assertEqual(resp.status_code, 401)
                self.assertEqual(resp.data, {'Error': 'Permission Denied'})
            elif user_type == "f":
                data["created_by_id"] = session.get('user_id')
                c = self.campaign_db_query(data)
                self.assertEqual(len(c), len(resp.data))
                self.assertEqual(resp.status_code, 200)
            elif user_type == "m":
                c = self.campaign_db_query(data)
                self.assertEqual(len(c), len(resp.data))
                self.assertEqual(resp.status_code, 200)

    #Test fails if the user is not authenticated
    def test_CUD_campaigns_not_authenticated(self):
        url = reverse('campaign:api-campaign')
        _post = self.client.post(url, format = 'json')
        _put = self.client.put(url, format = 'json')
        _del = self.client.delete(url, format = 'json')
        error = "Authentication credentials were not provided."
        self.assertEqual(_post.data["detail"] , error)
        self.assertEqual(_put.data["detail"] , error)
        self.assertEqual(_del.data["detail"] , error)
        self.assertNotEqual(_post.status_code, 200)
        self.assertNotEqual(_put.status_code, 200)
        self.assertNotEqual(_del.status_code, 200)

    #Test passes if the user is authenticated
    def test_CUD_campaigns_authenticated(self):
        for each_user_cred in user_cred:
            url = reverse('campaign:api-campaign')
            self.authenticate_user(each_user_cred)
            _post = self.client.post(url, format = 'json')
            _put = self.client.put(url, format = 'json')
            _del = self.client.delete(url, format = 'json')
            error = "Authentication credentials were not provided"
            self.assertNotEqual(_post.data.get("detail",None) , error)
            self.assertNotEqual(_put.data.get("detail",None) , error)
            self.assertNotEqual(_del.data.get("detail",None) , error)

    #Test fails if the donor is tring to post, put or delete data.
    def test_CUD_campaigns_donor(self):
        each_user_cred = {"username":"donor1","password":"donor1"}
        url = reverse('campaign:api-campaign')
        id = Campaign.objects.first().id
        data = {"id":id}
        self.authenticate_user(each_user_cred)
        _post = self.client.post(url,data, format = 'json')
        _put = self.client.put(url,data, format = 'json')
        error = "Permission Denied"
        self.assertEqual(_post.data.get("Error",None) , error)
        self.assertEqual(_put.data.get("Error",None) , error)


    #Test fails if title and description is not the part of post data
    def test_CUD_campaigns_post_title_and_description(self):
        each_user_cred = {"username":"fr1","password":"fr1"}
        url = reverse('campaign:api-campaign')
        first_id = Campaign.objects.first().id
        data={"id":first_id}
        login_resp = self.authenticate_user(each_user_cred)
        _post = self.client.post(url, format = 'json')
        _put = self.client.put(url, data, format = 'json')
        if "title" not in data:
            self.assertEqual( _post.data['title'][0] , "This field is required.")
            self.assertEqual(_post.status_code, 400)
            self.assertEqual( _put.data['title'][0] , "This field is required.")
            self.assertEqual(_put.status_code, 400)
        if "description" not in data:
            self.assertEqual( _post.data['description'][0] , "This field is required.")
            self.assertEqual(_post.status_code, 400)
            self.assertEqual( _put.data['description'][0] , "This field is required.")
            self.assertEqual(_put.status_code, 400)
        if "title" not in data and "description" not in data:
            self.assertEqual(_post.status_code, 400)
            self.assertEqual(_put.status_code, 400)

    #Test fails if amount or inventory is not the part of post data
    def test_CUD_campaigns_post_amount_or_inventory(self):
        each_user_cred = {"username":"fr1","password":"fr1"}
        url = reverse('campaign:api-campaign')
        first_id = Campaign.objects.first().id
        data={"title":"Test", "description":"Test2"}
        login_resp = self.authenticate_user(each_user_cred)
        _post = self.client.post(url,data, format = 'json')
        data["id"] = first_id
        _put = self.client.put(url,data, format = 'json')
        if "amount" not in data or "inventory" not in data:
            self.assertEqual( _post.data['non_field_errors'][0] , "Either amount or inventory must be provided")
            self.assertEqual(_post.status_code, 400)
            self.assertEqual( _put.data['non_field_errors'][0] , "Either amount or inventory must be provided")
            self.assertEqual(_put.status_code, 400)

    #Test passes if all required fields are passed
    def test_CUD_campaigns_post_success(self):
        each_user_cred = {"username":"fr1","password":"fr1"}
        url = reverse('campaign:api-campaign')
        data={"title":"Test123", "description":"Test123","inventory":["laptop"]}
        login_resp = self.authenticate_user(each_user_cred)
        _post = self.client.post(url,data, format = 'json')
        first_id = Campaign.objects.first().id
        data["id"] = first_id
        _put = self.client.put(url,data, format = 'json')
        self.assertEqual(_post.status_code, 201)
        self.assertEqual(_post.data, {'Success': 'Campaign Posted'})
        self.assertEqual(_put.status_code, 200)


    #Test passes if the created_by_id is correct
    def test_CUD_campaigns_post_created_by(self):
        each_user_cred = {"username":"fr2","password":"fr2"}
        url = reverse('campaign:api-campaign')
        data={"title":"Test1234", "description":"Test1234","inventory":["laptop"]}
        login_resp = self.authenticate_user(each_user_cred)
        resp = self.client.post(url,data, format = 'json')
        c = Campaign.objects.order_by('-created_on')[0]
        session = self.client.session
        user_id = session.get('user_id')
        self.assertEqual(c.created_by_id, User.objects.get(id=user_id))


    #Test fails if the unexpected inventory value is provided
    def test_CUD_campaigns_inventory_fail(self):
        each_user_cred = {"username":"fr1","password":"fr1"}
        url = reverse('campaign:api-campaign')
        data={"title":"Test123", "description":"Test123","inventory":"asd"}
        login_resp = self.authenticate_user(each_user_cred)
        _post = self.client.post(url,data, format = 'json')
        first_id = Campaign.objects.first().id
        data["id"] = first_id
        _put = self.client.put(url,data, format = 'json')
        self.assertNotEqual(_post.status_code, 201)
        self.assertNotEqual(_post.data, {'Success': 'Campaign Posted'})
        self.assertNotEqual(_put.status_code, 200)
        self.assertEqual(_post.data['inventory'][0]   , \
                        'Expected a list of items but got type "str".')
