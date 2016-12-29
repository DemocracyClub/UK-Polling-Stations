from rest_framework import serializers, viewsets
from councils.models import Council
# from .fields import PolygonField


class CouncilSerializer(serializers.HyperlinkedModelSerializer):
    # area = PolygonField()
    class Meta:
        model = Council
        fields = (
            'council_id', 'council_type', 'mapit_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address',
            # 'area' # This is super slow ATM - TODO!
        )


class CouncilViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.all()
    serializer_class = CouncilSerializer
