from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


@extend_schema_field(OpenApiTypes.OBJECT)
class PointField(serializers.Field):
    type_name = "PointField"
    type_label = "point"

    def to_representation(self, value):
        """
        Transform POINT object to a geojson feature.
        """
        if value is None:
            return value

        return {
            "type": "Feature",
            "properties": None,
            "geometry": {"type": "Point", "coordinates": [value.x, value.y]},
        }
