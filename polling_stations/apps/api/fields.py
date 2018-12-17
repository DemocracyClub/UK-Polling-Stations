from rest_framework import serializers


class PointField(serializers.Field):
    type_name = "PointField"
    type_label = "point"

    def to_representation(self, value):
        """
        Transform POINT object to a geojson feature.
        """
        if value is None:
            return value

        value = {
            "type": "Feature",
            "properties": None,
            "geometry": {"type": "Point", "coordinates": [value.x, value.y]},
        }
        return value
