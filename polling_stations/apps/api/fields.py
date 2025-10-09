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
        Value should be a dict with 'point' and 'properties' keys, where the values are a GEOS Point and a dict.
        """

        if value is None:
            return value

        point = value["point"]
        properties = value.get("properties", None)

        return {
            "type": "Feature",
            "properties": properties,
            "geometry": {"type": "Point", "coordinates": [point.x, point.y]},
        }
