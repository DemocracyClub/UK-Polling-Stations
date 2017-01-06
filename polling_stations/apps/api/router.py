from rest_framework import routers
from .address import ResidentialAddressViewSet
from .councils import CouncilViewSet
from .pollingdistricts import PollingDistrictViewSet
from .pollingstations import PollingStationViewSet
from .postcode import PostcodeViewSet


router = routers.DefaultRouter()
router.register(r'councils', CouncilViewSet)
router.register(r'pollingstations', PollingStationViewSet)
router.register(r'pollingdistricts', PollingDistrictViewSet)
router.register(r'postcode', PostcodeViewSet, base_name="postcode")
router.register(r'address', ResidentialAddressViewSet, base_name="address")
