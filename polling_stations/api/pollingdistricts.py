from rest_framework import serializers, viewsets
from pollingstations.models import PollingDistrict
# from .fields import PolygonField


class PollingDistrictSerializer(serializers.HyperlinkedModelSerializer):
    # area = PolygonField()
    class Meta:
        model = PollingDistrict
        fields = (
            'name', 'council',
            # 'area' This is super slow ATM - TODO!
        )


class PollingDistrictViewSet(viewsets.ModelViewSet):
    queryset = PollingDistrict.objects.all()
    serializer_class = PollingDistrictSerializer
