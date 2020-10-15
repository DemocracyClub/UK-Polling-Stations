from django.conf.urls import url
from rest_framework import routers
from .address import AddressViewSet
from .councils import CouncilViewSet
from .pollingdistricts import PollingDistrictViewSet
from .pollingstations import PollingStationViewSet
from .postcode import PostcodeViewSet
from .sandbox import SandboxView
from file_uploads.api import UploadViewSet


router = routers.DefaultRouter()
router.register(r"councils", CouncilViewSet)
router.register(r"pollingstations", PollingStationViewSet)
router.register(r"pollingdistricts", PollingDistrictViewSet)
router.register(r"postcode", PostcodeViewSet, basename="postcode")
router.register(r"address", AddressViewSet, basename="address")

router.urls.append(url(r"^uploads/", UploadViewSet.as_view({"post": "create"})))
router.urls.append(
    url(r"^sandbox/postcode/(?P<postcode>[A-Za-z0-9 +]+)/$", SandboxView.as_view())
)
router.urls.append(url(r"^sandbox/address/(?P<slug>[-\w]+)/$", SandboxView.as_view()))
