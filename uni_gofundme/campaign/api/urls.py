"""uni_gofundme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import ( CampaignCUDApiView,
                     CampaignRetrieveApiView,
                     RetrieveActiveCampaigns,
                     RetrieveOnWaitingCampaigns,
                    )

app_name = "campaign"

urlpatterns = [
    path('api/campaign', CampaignCUDApiView.as_view(), name="api-campaign"),
    path('api/campaign/list', CampaignRetrieveApiView.as_view(), name="api-campaign-list"),
    path('api/campaign/active', RetrieveActiveCampaigns.as_view(), name="api-campaign-active"),
    path('api/campaign/awaiting', RetrieveOnWaitingCampaigns.as_view(), name="api-campaign-awaiting"),
]
