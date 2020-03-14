from rest_framework import permissions
from campaign.models import CampaignStatusModel

class CampaignPostPermission(permissions.BasePermission):
    """
    Only fundraisers and mgo can post the campaigns
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated) and ( (request.user.type == "m")\
                or (request.user.type == "f") )

    def has_status_update_permission(self, request, view, post_obj):
        if 'status_type' in post_obj:
            print (post_obj)
            obj = CampaignStatusModel.objects.filter(status=post_obj['status_type'])
            if obj.exists():
                return (obj[0].id == 0) or (obj[0].id != 0 and\
                        request.user.type == 'm')
        return 1


class CampaignPutDelPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Also allows MGO to edit the campaings
    """
    def has_object_permission(self, request, view, obj):
        print ("*******E TERED", obj.owner , request.user)
        return (request.user.is_authenticated) and ( (obj.owner == \
                                request.user or request.user.type == 'm') )

    def has_status_update_permission(self, request, view, obj, upd_query):
        print (upd_query)
        print (upd_query['id'])
        print (obj.id)

        if 'status_type' in upd_query:
            upd_status_id = CampaignStatusModel.objects.filter(status=upd_query['status_type'])
            print (upd_status_id)
            return (upd_status_id[0].id != obj.id and \
                    request.user.type == 'm') or (upd_status_id[0].id == obj.id)

        return 1
