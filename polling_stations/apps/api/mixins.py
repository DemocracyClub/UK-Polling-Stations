from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000


class PollingEntityMixin:
    pagination_class = LargeResultsSetPagination

    def validate_request(self):
        if (
            self.id_field in self.request.query_params
            and "council_id" not in self.request.query_params
        ):
            return False
        return True

    def output(self, request):
        if not self.validate_request():
            return Response({"detail": "council_id parameter must be specified"}, 400)

        queryset = self.get_queryset()

        if "council_id" not in request.query_params:
            # paginate results if we are not filtering
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(
                    page, many=True, read_only=True, context={"request": request}
                )
                return self.get_paginated_response(serializer.data)

        if (
            "council_id" in request.query_params
            and self.id_field in request.query_params
            and len(queryset) == 1
        ):
            # If we are requesting a single polling station or district
            # return an object instead of an array with length 1
            serializer = self.get_serializer(
                queryset[0], many=False, read_only=True, context={"request": request}
            )
            return Response(serializer.data)

        if (
            "council_id" in request.query_params
            and self.id_field in request.query_params
            and len(queryset) == 0
        ):
            # If attempting to request a single polling station or district
            # which doesn't exist, return an error instead of an empty array
            return Response({"detail": "Not found"}, 404)

        serializer = self.get_serializer(
            queryset, many=True, read_only=True, context={"request": request}
        )
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        self.geo = False
        return self.output(request)

    @action(detail=False, url_path="geo")
    def geo(self, request, format=None):
        self.geo = True
        return self.output(request)


def parse_qs_to_python(qs: dict):
    qs = dict(qs)

    def _clean_value(v):
        if v in ["0", "false", "False"]:
            return False
        if v in ["1", "true", "True"]:
            return True
        return v

    for k, v in qs.items():
        if isinstance(v, list):
            sub_list = []
            for sub_v in v:
                sub_list.append(_clean_value(sub_v))
            qs[k] = sub_list
        else:
            qs[k] = _clean_value(v)
    return qs
