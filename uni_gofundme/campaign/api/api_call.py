import requests
import json

#Use django rest framework to get the reverse URLs.
url = 'http://192.168.5.125:8000/api/campaign/list'


class CampaignRetrieveAPICall(object):
    def get_campaign_by_id(id):
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data = json.dumps({"id":id}), headers=headers)
        return r.json()
