from rest_framework import routers
from .address import ResidentialAddressViewSet
from .councils import CouncilViewSet
from .pollingdistricts import PollingDistrictViewSet
from .pollingstations import PollingStationViewSet
from .postcode import PostcodeViewSet
from .sandbox import SandboxView


router = routers.DefaultRouter()
router.register(r'councils', CouncilViewSet)
router.register(r'pollingstations', PollingStationViewSet)
router.register(r'pollingdistricts', PollingDistrictViewSet)
router.register(r'postcode', PostcodeViewSet, basename="postcode")
router.register(r'address', ResidentialAddressViewSet, basename="address")


from django.conf.urls import url
router.urls.append(
    url(
        r"^sandbox/postcode/(?P<postcode>[A-Za-z0-9 +]+)/$",
        SandboxView.as_view()
    )
)
router.urls.append(
    url(
        r"^sandbox/address/(?P<slug>[-\w]+)/$",
        SandboxView.as_view()
    )
)
