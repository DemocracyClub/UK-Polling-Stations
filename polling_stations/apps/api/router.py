from django.urls import re_path
from file_uploads.api import UploadViewSet
from rest_framework import routers

from .address import AddressViewSet
from .councils import CouncilCSVViewSet, CouncilViewSet
from .pollingstations import PollingStationViewSet
from .postcode import PostcodeViewSet
from .sandbox import SandboxView

router = routers.DefaultRouter()
router.register(r"councils", CouncilViewSet)
router.register(
    r"council_csv",
    CouncilCSVViewSet,
    basename="council_csv",
)
router.register(r"pollingstations", PollingStationViewSet)
router.register(r"postcode", PostcodeViewSet, basename="postcode")
router.register(r"address", AddressViewSet, basename="address")

router.urls.append(re_path(r"^uploads/", UploadViewSet.as_view({"post": "create"})))
router.urls.append(
    re_path(r"^sandbox/postcode/(?P<postcode>[A-Za-z0-9 +]+)/$", SandboxView.as_view())
)
router.urls.append(
    re_path(r"^sandbox/address/(?P<slug>[-\w]+)/$", SandboxView.as_view())
)
